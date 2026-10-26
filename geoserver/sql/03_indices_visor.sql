-- Índices que necesita el visor de mapa de GDU (gdu/views/visor.py) sobre
-- tablas de catastro que Django no gestiona (managed=False), así que no hay
-- migración que los cree.
--
-- La vista visualizador.viviendas arma `ejecutores` y `planos` con subconsultas
-- correlacionadas por intervención; sin estos índices cada una recorre la tabla
-- entera una vez por fila devuelta (hasta MAX_FEATURES_POR_CAPA por pedido del
-- mapa). Con ellos el GeoJSON de Viviendas bajó de ~0.5 s a ~0.26 s.
--
-- Correr como el owner de las tablas (el DBUSER de polizador/.env, que es el
-- PG_APP_USER de la fase "postgres"); CREATE INDEX no necesita superusuario.
--
-- Idempotente: IF NOT EXISTS, se puede volver a correr sin efectos secundarios.
-- Sin CONCURRENTLY: son tablas chicas (~1.5k filas), el lock dura un instante.

\set ON_ERROR_STOP on

CREATE INDEX IF NOT EXISTS intervencion_ejecutor_id_intervencion_idx
    ON catastro.intervencion_ejecutor (id_intervencion);

CREATE INDEX IF NOT EXISTS plano_mensura_intervencion_idintervencion_idx
    ON catastro.plano_mensura_intervencion (idintervencion);

ANALYZE catastro.intervencion_ejecutor;
ANALYZE catastro.plano_mensura_intervencion;
