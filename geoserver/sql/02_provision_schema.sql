-- Esquema puente geoserver_auth (traduce Groups/Permissions de Django a roles
-- que GeoServer puede leer vía su servicio de roles JDBC) y permisos sobre las
-- capas piloto (catastro.localidad) para el datastore de GeoServer.
--
-- Correr como un usuario con privilegios para crear el schema y hacer GRANT
-- sobre catastro.* (el owner de la base, ej. DBUSER de polizador/.env alcanza;
-- no requiere superusuario). Los roles geoserver_piloto y geoserver_security
-- tienen que existir ya -- correr antes 01_provision_roles.sql (ese sí necesita
-- superusuario).
--
-- Idempotente: DROP VIEW + CREATE VIEW en cada corrida, así que se puede volver
-- a correr después de cambios en las vistas sin efectos secundarios.
--
-- El bridge 'admin' -> 'ADMIN' es necesario: 'admin' es el usuario local de
-- GeoServer (no existe en Django), y sin este puente, activar este servicio de
-- roles como "Active role service" en GeoServer deja al admin sin ningún rol
-- -> lockout del panel de administración. No lo saques sin dejar otra forma de
-- que 'admin' resuelva a ADMIN.

\set ON_ERROR_STOP on

CREATE SCHEMA IF NOT EXISTS geoserver_auth;

DROP VIEW IF EXISTS geoserver_auth.roles;
CREATE VIEW geoserver_auth.roles AS
SELECT DISTINCT upper(regexp_replace(name::text, '[^A-Za-z0-9]+'::text, '_'::text, 'g'::text)) AS name,
    NULL::text AS parent
FROM auth_group
UNION
SELECT 'ADMIN' AS name, NULL::text AS parent;

DROP VIEW IF EXISTS geoserver_auth.user_roles;
CREATE VIEW geoserver_auth.user_roles AS
SELECT u.username::varchar(150) AS username,
    upper(regexp_replace(g.name::text, '[^A-Za-z0-9]+'::text, '_'::text, 'g'::text)) AS rolename
FROM personalizador_customuser u
    JOIN personalizador_customuser_groups ug ON ug.customuser_id = u.id
    JOIN auth_group g ON g.id = ug.group_id
WHERE u.is_active
UNION
SELECT 'admin'::varchar(150) AS username, 'ADMIN' AS rolename;

GRANT USAGE ON SCHEMA geoserver_auth TO geoserver_security;
GRANT SELECT ON geoserver_auth.roles, geoserver_auth.user_roles TO geoserver_security;

-- Acceso de lectura/escritura del datastore sobre las capas geométricas
-- publicadas (Fase 1: localidad; Fase 4a: + manzana/calle/vivienda_punto,
-- mismo patrón de tabla -- id serial, geom SRID 22175, updated_by/updated_at
-- con el trigger catastro.set_updated() de más abajo). Al publicar una capa
-- nueva, agregar acá su GRANT (tabla + secuencia) y sumar sus reglas en
-- templates/layers.properties.
GRANT USAGE ON SCHEMA catastro TO geoserver_piloto;
GRANT SELECT, INSERT, UPDATE, DELETE ON catastro.localidad, catastro.manzana, catastro.calle, catastro.vivienda_punto TO geoserver_piloto;
GRANT USAGE, SELECT ON catastro.localidad_id_seq, catastro.manzana_id_seq, catastro.calle_id_seq, catastro.vivienda_punto_id_seq TO geoserver_piloto;

-- Spike N:N (Intervención: relaciones "inspectores"/"ejecutores", ver
-- forms/nn.py): intervencion/inspector/ejecutor no tienen geometría propia,
-- pero sí el mismo trigger catastro.set_updated() de más abajo. Las tablas
-- intermedias son las que nn.py escribe directo vía
-- dataProvider().addFeatures()/deleteFeatures() -- intervencion_inspector no
-- tiene updated_by/updated_at (solo 2 FKs), intervencion_ejecutor sí.
GRANT SELECT, INSERT, UPDATE, DELETE ON catastro.intervencion, catastro.inspector, catastro.ejecutor, catastro.intervencion_inspector, catastro.intervencion_ejecutor TO geoserver_piloto;
GRANT USAGE, SELECT ON catastro.intervencion_id_seq, catastro.inspector_id_seq, catastro.ejecutor_id_seq, catastro.intervencion_inspector_id_seq, catastro.intervencion_ejecutor_id_seq TO geoserver_piloto;

-- plano_mensura/tierra (generalización posterior al spike N:N): plano_mensura
-- y tierra tienen geometría propia (Polygon); las tablas intermedias
-- plano_mensura_intervencion/plano_mensura_tierra no tienen updated_by
-- (mismo patrón que intervencion_inspector). Probado en vivo que las columnas
-- de tipo enum custom de Postgres (tipo_plano_mensura en las intermedias;
-- tipo/tipo_oferente/tipo_inscripcion/localizacion/superficie/estado en
-- tierra) se exponen y escriben como texto plano vía WFS sin problema.
GRANT SELECT, INSERT, UPDATE, DELETE ON catastro.plano_mensura, catastro.plano_mensura_intervencion, catastro.tierra, catastro.plano_mensura_tierra TO geoserver_piloto;
GRANT USAGE, SELECT ON catastro.plano_mensura_id_seq, catastro.plano_mensura_intervencion_id_seq, catastro.tierra_id_seq, catastro.plano_mensura_tierra_id_seq TO geoserver_piloto;

-- catastro.set_updated() es el trigger BEFORE INSERT/UPDATE compartido por
-- las ~30 tablas de catastro (incluida localidad) que pisaba
-- "NEW.updated_by = current_user" incondicionalmente -- current_user es
-- siempre geoserver_piloto para cualquier escritura que venga de GeoServer,
-- así que no distinguía usuarios reales. Con COALESCE, si el plugin
-- ../plugin/gdu-updated-by-listener.jar ya puso el usuario autenticado real
-- en la columna antes de que llegue el UPDATE/INSERT, el trigger lo
-- respeta; si no vino nada (ej. una escritura fuera de GeoServer), sigue
-- cayendo a current_user como antes -- no rompe nada para las ~29 tablas
-- que todavía no pasan por WFS-T.
CREATE OR REPLACE FUNCTION catastro.set_updated() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = NOW();
  NEW.updated_by = COALESCE(NEW.updated_by, current_user);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
