-- Esquema (solo DDL) de la base GDU heredada (dump de Hasura), para los tests del ETL.
-- Generado con pg_dump -s -n public -n our -n audit -n visualizador --no-owner --no-privileges
-- sobre el dump restaurado; se quitaron CREATE SCHEMA public, el set_config de search_path
-- y los metacomandos \restrict de psql.
--
-- PostgreSQL database dump
--


-- Dumped from database version 17.10 (Ubuntu 17.10-0ubuntu0.25.10.1)
-- Dumped by pg_dump version 17.10 (Ubuntu 17.10-0ubuntu0.25.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: audit; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA audit;


--
-- Name: our; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA our;


--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--



--
-- Name: visualizador; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA visualizador;


--
-- Name: adjudicacion_beneficiario_tipo; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.adjudicacion_beneficiario_tipo AS ENUM (
    'Provisoria',
    'Definitiva'
);


--
-- Name: gestion_expropiacion; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.gestion_expropiacion AS ENUM (
    'Ipduv',
    'Externa'
);


--
-- Name: parcela_estado_dominial; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.parcela_estado_dominial AS ENUM (
    'Propietario',
    'IPDUV',
    'Adjudicatario',
    'Municipio'
);


--
-- Name: parcela_estado_dominial_2; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.parcela_estado_dominial_2 AS ENUM (
    'Propietario',
    'IPDUV',
    'Estado Provincial',
    'Privado',
    'Verificar',
    'Donado',
    'Estado Nacional',
    'Estado Municipal'
);


--
-- Name: resolucion_costos_tipo; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.resolucion_costos_tipo AS ENUM (
    'Provisoria',
    'Definitiva'
);


--
-- Name: tierra_estado_ocupacion; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_estado_ocupacion AS ENUM (
    'libre',
    'parcialmente_ocupado',
    'ocupado'
);


--
-- Name: tierra_localizacion; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_localizacion AS ENUM (
    'central',
    'intermedia',
    'periferica'
);


--
-- Name: tierra_proy_loteo; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_proy_loteo AS ENUM (
    'No Presentado',
    'Presentado',
    'Con Observaciones',
    'Sin Observaciones'
);


--
-- Name: tierra_superficie; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_superficie AS ENUM (
    '0-200',
    '200-500',
    '500+'
);


--
-- Name: tierra_tipo; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_tipo AS ENUM (
    'ipduv',
    'terceros'
);


--
-- Name: tierra_tipo_inscripcion; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_tipo_inscripcion AS ENUM (
    'folio_real',
    'tomo_folio_finca_ano',
    'articulo_ley'
);


--
-- Name: tierra_tipo_oferente; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tierra_tipo_oferente AS ENUM (
    'provincia',
    'municipio',
    'entidad_intermedia',
    'particular'
);


--
-- Name: tipo_id_adjudicatario; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tipo_id_adjudicatario AS ENUM (
    'DNI',
    'NRO ADJUDICATARIO'
);


--
-- Name: tipo_plano_mensura; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tipo_plano_mensura AS ENUM (
    'perimetral',
    'subdivision'
);


--
-- Name: cargarviviendas(integer); Type: FUNCTION; Schema: our; Owner: -
--

CREATE FUNCTION our.cargarviviendas(rel integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	r record;
BEGIN

	DELETE FROM our.vivienda WHERE relevamiento = rel;
	FOR r IN (
		SELECT jsonb_array_elements(viviendas->'features') as registro
		FROM our.relevamiento
		WHERE id = rel
	)
	LOOP

	INSERT INTO our.vivienda(
	relevamiento,
	vivienda,
	geom,
	properties,
	relevado
	)
	VALUES (
		rel,
		(r.registro->'properties'->'id')::integer,
		st_geomfromgeojson(r.registro->'geometry' || '{"crs":{"type":"name","properties":{"name":"EPSG:3857"}}}'::jsonb),
		r.registro->'properties',
		(r.registro->'properties'->'relevado')::boolean
		);

	RAISE NOTICE '%', r.registro;
	END LOOP;
  
  RETURN 1;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: variables_encuesta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.variables_encuesta (
    id_pregunta integer,
    variable character varying(255),
    tipo_dato character varying(255),
    tipo_pregunta integer,
    respuestas text[]
);


--
-- Name: datos_encuesta(integer, integer); Type: FUNCTION; Schema: our; Owner: -
--

CREATE FUNCTION our.datos_encuesta(id_vivienda integer, id_relevamiento integer) RETURNS SETOF our.variables_encuesta
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
	RETURN QUERY
	SELECT pr.id AS id_pregunta,
    pr.variable,
    -- re.encuesta,
    -- re.valor,
    tp.tipo AS tipo_dato,
    p.tipo AS tipo_pregunta,
	ARRAY_AGG(re.valor) as respuestas
   FROM our.pregunta_relevamiento pr
     LEFT JOIN (
	 	SELECT * FROM
	 	our.respuesta_encuesta re 
		INNER JOIN our.encuesta e ON re.encuesta = e.id
		WHERE e.vivienda = id_vivienda AND e.relevamiento = id_relevamiento
		
		 
	 ) as re 
	 ON re.pregunta = pr.id
     LEFT JOIN our.respuesta r ON r.id = re.respuesta
     LEFT JOIN our.pregunta p ON p.id = pr.pregunta
     LEFT JOIN our.tipo_pregunta tp ON tp.id = p.tipo
	 GROUP BY 1,2,3,4;
END;
$$;


--
-- Name: gj_registros; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.gj_registros (
    gj json
);


--
-- Name: gj_viviendas(integer); Type: FUNCTION; Schema: our; Owner: -
--

CREATE FUNCTION our.gj_viviendas(rel integer) RETURNS SETOF our.gj_registros
    LANGUAGE sql STABLE
    AS $$ 
SELECT
  json_build_object(
    'type', 'FeatureCollection',
	'crs', '{"type":"name","properties":{"name":"EPSG:3857"}}'::jsonb,
    'features', 
		json_agg(
			json_build_object(
				'type', 'Feature',
				'properties', v.properties,
				'geometry', ST_AsGeoJSON(v.geom)::jsonb- 'crs'
			) 
		)
  ) as gj
FROM our.vivienda v

WHERE relevamiento = rel;
$$;


--
-- Name: update_vivienda_relevado(); Type: FUNCTION; Schema: our; Owner: -
--

CREATE FUNCTION our.update_vivienda_relevado() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	u record; -- uf
	p record; -- parcela
	cant integer; 
BEGIN


	UPDATE our.vivienda 
	SET relevado = TRUE, 
	properties = properties || '{"relevado": true}'
	WHERE vivienda = NEW.vivienda 
	AND relevamiento = NEW.relevamiento ;

	RETURN NULL; -- result is ignored since this is an AFTER trigger
  
  
END;
$$;


--
-- Name: set_es_ph(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_es_ph() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	u record; -- uf
	p record; -- parcela
	cant integer; 
BEGIN
   IF (TG_OP = 'DELETE') THEN
	    RAISE NOTICE 'DELETE';
		FOR u IN (
			SELECT DISTINCT id_parcela FROM old_table
		)LOOP
			RAISE NOTICE 'u: %', u.id_parcela;
			
			SELECT COUNT(id) INTO cant FROM uf WHERE id_parcela = u.id_parcela;
			IF cant > 1 THEN
				UPDATE parcela SET es_ph = TRUE WHERE id = u.id_parcela;
			ELSE
				UPDATE parcela SET es_ph = FALSE WHERE id = u.id_parcela;
			END IF;
			RAISE NOTICE 'cant: %', cant;
			
		END LOOP;
		
	ELSIF (TG_OP = 'UPDATE') THEN
		RAISE NOTICE 'UPDATE';
		
		FOR u IN (
			SELECT DISTINCT id_parcela FROM (
				SELECT * FROM old_table 
				UNION
				SELECT * FROM new_table
			) as todo
		)LOOP
			RAISE NOTICE 'u: %', u.id_parcela;
			
			SELECT COUNT(id) INTO cant FROM uf WHERE id_parcela = u.id_parcela;
			IF cant > 1 THEN
				UPDATE parcela SET es_ph = TRUE WHERE id = u.id_parcela;
			ELSE
				UPDATE parcela SET es_ph = FALSE WHERE id = u.id_parcela;
			END IF;
			RAISE NOTICE 'cant: %', cant;
			
		END LOOP;
		
		
		
	ELSIF (TG_OP = 'INSERT') THEN
		RAISE NOTICE 'INSERT';
		FOR u IN (
			SELECT DISTINCT id_parcela FROM new_table
		)LOOP
			RAISE NOTICE 'u: %', u.id_parcela;
			
			SELECT COUNT(id) INTO cant FROM uf WHERE id_parcela = u.id_parcela;
			IF cant > 1 THEN
				UPDATE parcela SET es_ph = TRUE WHERE id = u.id_parcela;
			ELSE
				UPDATE parcela SET es_ph = FALSE WHERE id = u.id_parcela;
			END IF;
			RAISE NOTICE 'cant: %', cant;
			
		END LOOP;
	END IF;
	RETURN NULL; -- result is ignored since this is an AFTER trigger
  
  
  
END;
$$;


--
-- Name: set_lonlat(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_lonlat() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.longitud = ST_X(ST_Transform(NEW.geom,4326));
  NEW.latitud = ST_Y(ST_Transform(NEW.geom,4326));
  RETURN NEW;
END;
$$;


--
-- Name: set_nomenclatura(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_nomenclatura() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
  NEW.nomenclatura = NEW.dpto || NEW.circ || NEW.secc || NEW.ch|| 
  NEW.qta || NEW.fracc || NEW.mz || NEW.parc  ;
  
  RETURN NEW;
END;$$;


--
-- Name: set_updated(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_updated() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = NOW();
  NEW.updated_by = current_user;
  RETURN NEW;
END;
$$;


--
-- Name: update_frm_mat(character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_frm_mat(nc character varying, nuevo_fr_mat character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
        r record;
BEGIN
FOR r IN (
		SELECT uf.id, uf.fr_mat FROM parcela p INNER JOIN uf 
		ON p.id = uf.id_parcela
		WHERE p.nomenclatura = nc
	)
	LOOP
		IF r.fr_mat IS NULL OR TRIM(r.fr_mat) = '' THEN
			UPDATE uf SET fr_mat = nuevo_fr_mat WHERE id = r.id;
			RAISE NOTICE 'encontrado(%)',  r.fr_mat;
			
		END IF;
	
	END LOOP;
END;

$$;


--
-- Name: update_nro_adjudicatario(integer, integer, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_nro_adjudicatario(p_plan integer, p_grupo integer, p_mz character varying, p_parc character varying, nro_adj integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
        r record;
BEGIN
FOR r IN (
		SELECT * FROM vistas.viviendas v WHERE 
		v.plan = p_plan AND v.grupo = p_grupo AND
		v.mz = LPAD(p_mz,4,'0') AND v.parc = LPAD(p_parc, 5, '0')	
	)
	LOOP
			UPDATE uf SET nro_adjudicatario = nro_adj 
			WHERE uf.id = r.id;
			RAISE NOTICE 'encontrado(%)',  r.id;
	END LOOP;
END;

$$;


--
-- Name: audit_logs; Type: TABLE; Schema: audit; Owner: -
--

CREATE TABLE audit.audit_logs (
    id bigint NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    user_id integer NOT NULL,
    username character varying(255) NOT NULL,
    action character varying(255) NOT NULL,
    client_addr inet,
    metadata jsonb
);


--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: audit; Owner: -
--

CREATE SEQUENCE audit.audit_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: audit; Owner: -
--

ALTER SEQUENCE audit.audit_logs_id_seq OWNED BY audit.audit_logs.id;


--
-- Name: encuesta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.encuesta (
    id integer NOT NULL,
    relevamiento integer NOT NULL,
    vivienda integer NOT NULL,
    "user" character varying,
    tstamp timestamp without time zone,
    tipo integer
);


--
-- Name: encuesta_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.encuesta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: encuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.encuesta_id_seq OWNED BY our.encuesta.id;


--
-- Name: pregunta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.pregunta (
    id integer NOT NULL,
    tipo integer NOT NULL,
    texto text NOT NULL,
    subtexto text
);


--
-- Name: pregunta_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.pregunta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pregunta_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.pregunta_id_seq OWNED BY our.pregunta.id;


--
-- Name: pregunta_relevamiento; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.pregunta_relevamiento (
    id integer NOT NULL,
    relevamiento integer NOT NULL,
    seccion integer NOT NULL,
    pregunta integer NOT NULL,
    variable character varying(255) NOT NULL,
    visible text,
    valido text,
    required boolean DEFAULT true NOT NULL
);


--
-- Name: pregunta_relevamiento_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.pregunta_relevamiento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 10
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pregunta_relevamiento_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.pregunta_relevamiento_id_seq OWNED BY our.pregunta_relevamiento.id;


--
-- Name: relevamiento; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.relevamiento (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    fecha date DEFAULT now() NOT NULL,
    descripcion text,
    objetivo integer DEFAULT 0 NOT NULL,
    viviendas jsonb,
    barrios jsonb
);


--
-- Name: relevamiento_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.relevamiento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: relevamiento_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.relevamiento_id_seq OWNED BY our.relevamiento.id;


--
-- Name: respuesta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.respuesta (
    id integer NOT NULL,
    pregunta integer NOT NULL,
    texto character varying(255) NOT NULL,
    nro_opcion integer NOT NULL,
    valor text NOT NULL
);


--
-- Name: respuesta_encuesta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.respuesta_encuesta (
    id integer NOT NULL,
    encuesta integer NOT NULL,
    pregunta integer NOT NULL,
    respuesta integer,
    valor text NOT NULL
);


--
-- Name: respuesta_encuesta_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.respuesta_encuesta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: respuesta_encuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.respuesta_encuesta_id_seq OWNED BY our.respuesta_encuesta.id;


--
-- Name: respuesta_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.respuesta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: respuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.respuesta_id_seq OWNED BY our.respuesta.id;


--
-- Name: tipo_pregunta; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.tipo_pregunta (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    tipo character varying(255) NOT NULL,
    descripcion text
);


--
-- Name: resultados_encuesta; Type: VIEW; Schema: our; Owner: -
--

CREATE VIEW our.resultados_encuesta AS
 SELECT pr.id AS id_pregunta,
    pr.variable,
    re.encuesta,
    re.valor,
    tp.tipo AS tipo_dato,
    p.tipo AS tipo_pregunta,
        CASE
            WHEN (p.tipo = 5) THEN (
            CASE
                WHEN (re.valor = 'true'::text) THEN 'SI'::text
                ELSE 'NO'::text
            END)::character varying
            WHEN (p.tipo = ANY (ARRAY[1, 2, 9])) THEN r.texto
            ELSE (re.valor)::character varying
        END AS respuesta
   FROM ((((our.pregunta_relevamiento pr
     LEFT JOIN our.respuesta_encuesta re ON ((re.pregunta = pr.id)))
     LEFT JOIN our.respuesta r ON ((r.id = re.respuesta)))
     JOIN our.pregunta p ON ((p.id = pr.pregunta)))
     JOIN our.tipo_pregunta tp ON ((tp.id = p.tipo)));


--
-- Name: resultados_pregunta; Type: VIEW; Schema: our; Owner: -
--

CREATE VIEW our.resultados_pregunta AS
 SELECT pr.id AS pregunta,
    re.respuesta AS id_respuesta,
    re.valor,
        CASE
            WHEN (p.tipo = 5) THEN
            CASE
                WHEN (re.valor = 'true'::text) THEN 'SI'::text
                ELSE 'NO'::text
            END
            WHEN (p.tipo = ANY (ARRAY[1, 2, 9])) THEN (r.texto)::text
            ELSE re.valor
        END AS respuesta,
    count(*) AS cantidad
   FROM (((our.pregunta_relevamiento pr
     JOIN our.respuesta_encuesta re ON ((re.pregunta = pr.id)))
     LEFT JOIN our.pregunta p ON ((p.id = pr.pregunta)))
     LEFT JOIN our.respuesta r ON ((r.id = re.respuesta)))
  WHERE (p.tipo <> ALL (ARRAY[6, 7, 8, 10]))
  GROUP BY pr.id, re.respuesta, re.valor,
        CASE
            WHEN (p.tipo = 5) THEN
            CASE
                WHEN (re.valor = 'true'::text) THEN 'SI'::text
                ELSE 'NO'::text
            END
            WHEN (p.tipo = ANY (ARRAY[1, 2, 9])) THEN (r.texto)::text
            ELSE re.valor
        END
  ORDER BY pr.id, re.respuesta;


--
-- Name: seccion; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.seccion (
    id integer NOT NULL,
    relevamiento integer NOT NULL,
    nombre character varying(255) NOT NULL,
    texto text,
    orden integer NOT NULL,
    visible text
);


--
-- Name: seccion_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.seccion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: seccion_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.seccion_id_seq OWNED BY our.seccion.id;


--
-- Name: tipo_pregunta_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.tipo_pregunta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_pregunta_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.tipo_pregunta_id_seq OWNED BY our.tipo_pregunta.id;


--
-- Name: vivienda; Type: TABLE; Schema: our; Owner: -
--

CREATE TABLE our.vivienda (
    id integer NOT NULL,
    relevamiento integer NOT NULL,
    vivienda integer NOT NULL,
    geom public.geometry(MultiPolygon,3857) NOT NULL,
    properties jsonb DEFAULT '{}'::jsonb NOT NULL,
    relevado boolean DEFAULT false NOT NULL
);


--
-- Name: vivienda_id_seq; Type: SEQUENCE; Schema: our; Owner: -
--

CREATE SEQUENCE our.vivienda_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vivienda_id_seq; Type: SEQUENCE OWNED BY; Schema: our; Owner: -
--

ALTER SEQUENCE our.vivienda_id_seq OWNED BY our.vivienda.id;


--
-- Name: actuacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.actuacion (
    id integer NOT NULL,
    id_programa integer NOT NULL,
    ano integer NOT NULL,
    nombre character varying(255) NOT NULL,
    instrumento character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: actuacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.actuacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: actuacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.actuacion_id_seq OWNED BY public.actuacion.id;


--
-- Name: adjudicacion_beneficiario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.adjudicacion_beneficiario (
    id integer NOT NULL,
    nro character varying(255) NOT NULL,
    ano integer NOT NULL,
    tipo public.adjudicacion_beneficiario_tipo NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: adjudicacion_beneficiario_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.adjudicacion_beneficiario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: adjudicacion_beneficiario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.adjudicacion_beneficiario_id_seq OWNED BY public.adjudicacion_beneficiario.id;


--
-- Name: adjudicatario3450; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.adjudicatario3450 (
    "AdjuGISNroAdju" integer NOT NULL,
    "AdjuGISEscritura" character varying(2),
    "AdjuGISResActa" character varying(255),
    "AdjuGISResFecha" date,
    "AdjuGISResNro" integer,
    "AdjuGISapeynom" character varying(255),
    "AdjuGISdireccion" character varying(255),
    "AdjuGISdni" integer,
    "AdjuGISmatricula" character varying(255),
    "AdjuGISmotivo" character varying(255),
    "AdjuGISsituacion" character varying(255),
    "AdjuGISEstadoReg" character varying(255)
);


--
-- Name: barrio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.barrio (
    id integer NOT NULL,
    id_intervencion integer NOT NULL,
    nombre character varying(255),
    geom public.geometry(MultiPolygon,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: barrio_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.barrio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: barrio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.barrio_id_seq OWNED BY public.barrio.id;


--
-- Name: calle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.calle (
    id integer NOT NULL,
    id_intervencion integer NOT NULL,
    nombre character varying(255),
    geom public.geometry(LineString,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: calle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.calle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: calle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.calle_id_seq OWNED BY public.calle.id;


--
-- Name: catastrourbano; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.catastrourbano (
    id integer NOT NULL,
    id_nomencl character varying(29),
    plano_apro character varying(11),
    dpto character varying(2),
    circ character varying(3),
    secc character varying(2),
    ch character varying(4),
    qta character varying(4),
    fracc character varying(4),
    mz character varying(5),
    parc character varying(5),
    matric character varying(6),
    tomo integer,
    folio integer,
    finca integer,
    anio integer,
    municipio character varying(254),
    geom public.geometry(Polygon,22175)
);


--
-- Name: catastrourbano_gid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.catastrourbano_gid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: catastrourbano_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.catastrourbano_gid_seq OWNED BY public.catastrourbano.id;


--
-- Name: contratacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contratacion (
    id integer NOT NULL,
    id_actuacion integer NOT NULL,
    tipo integer NOT NULL,
    expediente character varying(255),
    resolucion character varying(255),
    ano integer NOT NULL,
    nombre character varying(255),
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: contratacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contratacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contratacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contratacion_id_seq OWNED BY public.contratacion.id;


--
-- Name: departamento; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departamento (
    gid integer NOT NULL,
    id integer,
    nombre character varying(80),
    geom public.geometry(MultiPolygon,22175),
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: departamento_gid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.departamento_gid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: departamento_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.departamento_gid_seq OWNED BY public.departamento.gid;


--
-- Name: destino_parcela; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.destino_parcela (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: destino_parcela_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.destino_parcela_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: destino_parcela_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.destino_parcela_id_seq OWNED BY public.destino_parcela.id;


--
-- Name: ejecutor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ejecutor (
    id integer NOT NULL,
    tipo integer NOT NULL,
    cuit character(11) NOT NULL,
    nombre character varying(255) NOT NULL,
    direccion character varying(255),
    id_localidad integer,
    nombre_contacto character varying(255),
    telefono_contacto character varying(255),
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: ejecutor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ejecutor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ejecutor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ejecutor_id_seq OWNED BY public.ejecutor.id;


--
-- Name: estado_dominial; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estado_dominial (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text
);


--
-- Name: estado_dominial_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estado_dominial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estado_dominial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estado_dominial_id_seq OWNED BY public.estado_dominial.id;


--
-- Name: estado_gestion_expropiacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estado_gestion_expropiacion (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL
);


--
-- Name: estado_gestion_expropiacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.estado_gestion_expropiacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: estado_gestion_expropiacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.estado_gestion_expropiacion_id_seq OWNED BY public.estado_gestion_expropiacion.id;


--
-- Name: expropiacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.expropiacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: expropiacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.expropiacion (
    id integer DEFAULT nextval('public.expropiacion_id_seq'::regclass) NOT NULL,
    nro_ley integer NOT NULL,
    ano_ley integer,
    ley_prorrogas character varying(255),
    localidad integer NOT NULL,
    asentamiento_nombre character varying(255),
    letra_ley character(1),
    asentamiento boolean NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    gestion public.gestion_expropiacion DEFAULT 'Ipduv'::public.gestion_expropiacion NOT NULL
);


--
-- Name: infraestructura_linea; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.infraestructura_linea (
);


--
-- Name: infraestructura_punto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.infraestructura_punto (
);


--
-- Name: inspector; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inspector (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: inspector_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inspector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inspector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inspector_id_seq OWNED BY public.inspector.id;


--
-- Name: intervencion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intervencion (
    id integer NOT NULL,
    id_localidad integer NOT NULL,
    id_contratacion integer NOT NULL,
    nombre character varying(255) NOT NULL,
    tipo integer NOT NULL,
    avance numeric(10,2),
    estado integer,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    grupo character varying(255),
    drf_plan integer,
    drf_grupo integer,
    id_adjudicacion integer
);


--
-- Name: intervencion_ejecutor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intervencion_ejecutor (
    id_intervencion integer NOT NULL,
    id_ejecutor integer NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    id integer NOT NULL
);


--
-- Name: intervencion_ejecutor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.intervencion_ejecutor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: intervencion_ejecutor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.intervencion_ejecutor_id_seq OWNED BY public.intervencion_ejecutor.id;


--
-- Name: intervencion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.intervencion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: intervencion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.intervencion_id_seq OWNED BY public.intervencion.id;


--
-- Name: intervencion_inspector; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intervencion_inspector (
    id integer NOT NULL,
    idintervencion integer NOT NULL,
    idinspector integer NOT NULL
);


--
-- Name: intervencion_inspector_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.intervencion_inspector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: intervencion_inspector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.intervencion_inspector_id_seq OWNED BY public.intervencion_inspector.id;


--
-- Name: layer_styles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.layer_styles (
    id integer NOT NULL,
    f_table_catalog character varying,
    f_table_schema character varying,
    f_table_name character varying,
    f_geometry_column character varying,
    stylename text,
    styleqml xml,
    stylesld xml,
    useasdefault boolean,
    description text,
    owner character varying(63) DEFAULT CURRENT_USER,
    ui xml,
    update_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    type character varying
);


--
-- Name: layer_styles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.layer_styles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: layer_styles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.layer_styles_id_seq OWNED BY public.layer_styles.id;


--
-- Name: localidad; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.localidad (
    id integer NOT NULL,
    codpcia character(2) NOT NULL,
    coddpto character(3) NOT NULL,
    codloc character(3) NOT NULL,
    provincia character varying(255) NOT NULL,
    departamento character varying(255) NOT NULL,
    localidad character varying(255) NOT NULL,
    geom public.geometry(Point,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: localidad_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.localidad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: localidad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.localidad_id_seq OWNED BY public.localidad.id;


--
-- Name: manzana; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.manzana (
    id integer NOT NULL,
    id_intervencion integer NOT NULL,
    nombre character varying(255) NOT NULL,
    geom public.geometry(Polygon,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: manzana_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.manzana_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: manzana_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.manzana_id_seq OWNED BY public.manzana.id;


--
-- Name: municipio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipio (
    id integer NOT NULL,
    nombre character varying(80),
    depto character varying(80),
    region integer,
    udt integer,
    categoria integer,
    cod_indec bigint,
    geom public.geometry(MultiPolygon,22175),
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: objeto_expropiacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.objeto_expropiacion (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: objeto_expropiacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.objeto_expropiacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: objeto_expropiacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.objeto_expropiacion_id_seq OWNED BY public.objeto_expropiacion.id;


--
-- Name: parcela; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parcela (
    id integer NOT NULL,
    id_intervencion integer NOT NULL,
    nomenclatura character(28),
    dpto character(2) NOT NULL,
    circ character(3) NOT NULL,
    secc character(2) NOT NULL,
    ch character(4) NOT NULL,
    qta character(4) NOT NULL,
    fracc character(4) NOT NULL,
    mz character(4) NOT NULL,
    parc character(5) NOT NULL,
    geom public.geometry(Polygon,22175) NOT NULL,
    destino integer NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    estado_dominial public.parcela_estado_dominial_2,
    es_ph boolean DEFAULT false NOT NULL
);


--
-- Name: parcela_expropiada_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.parcela_expropiada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: parcela_expropiada; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parcela_expropiada (
    id integer DEFAULT nextval('public.parcela_expropiada_id_seq'::regclass) NOT NULL,
    id_expropiacion integer NOT NULL,
    nomenclatura character(28) NOT NULL,
    dpto character(2) NOT NULL,
    circ character(3) NOT NULL,
    secc character(2) NOT NULL,
    ch character(4) NOT NULL,
    qta character(4) NOT NULL,
    fracc character(4) NOT NULL,
    mz character(4) NOT NULL,
    parc character(5) NOT NULL,
    propietario_actual character varying(255),
    inscripcion character varying(255),
    estado_gestion integer NOT NULL,
    observaciones text,
    geom public.geometry(Polygon,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    objeto integer NOT NULL,
    propietario_expropiado character varying(255),
    regularizable text
);


--
-- Name: parcela_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.parcela_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: parcela_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.parcela_id_seq OWNED BY public.parcela.id;


--
-- Name: plano_mensura; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plano_mensura (
    id integer NOT NULL,
    depto character(2) NOT NULL,
    nro integer NOT NULL,
    ano character(2) NOT NULL,
    pm_antecedente character varying(255),
    en_gdu boolean,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    sup_parcelas numeric(10,2),
    sup_calles numeric(10,2),
    sup_reserva numeric(10,2),
    geom public.geometry(Polygon,22175)
);


--
-- Name: plano_mensura_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.plano_mensura_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: plano_mensura_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.plano_mensura_id_seq OWNED BY public.plano_mensura.id;


--
-- Name: plano_mensura_intervencion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plano_mensura_intervencion (
    id integer NOT NULL,
    idplano integer NOT NULL,
    idintervencion integer NOT NULL,
    tipo public.tipo_plano_mensura NOT NULL
);


--
-- Name: plano_mensura_intervencion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.plano_mensura_intervencion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: plano_mensura_intervencion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.plano_mensura_intervencion_id_seq OWNED BY public.plano_mensura_intervencion.id;


--
-- Name: plano_mensura_tierra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plano_mensura_tierra (
    id integer NOT NULL,
    idplano integer NOT NULL,
    idtierra integer NOT NULL,
    tipo public.tipo_plano_mensura NOT NULL
);


--
-- Name: plano_mensura_tierra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.plano_mensura_tierra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: plano_mensura_tierra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.plano_mensura_tierra_id_seq OWNED BY public.plano_mensura_tierra.id;


--
-- Name: pre_adjudicatario_dispersa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pre_adjudicatario_dispersa (
    id integer NOT NULL,
    apellido character varying(255) NOT NULL,
    nombre character varying(255) NOT NULL,
    genero character varying(255),
    documento integer,
    cantidad_personas integer,
    inscripcion character varying(255),
    plano_mensura character varying(255),
    propietario character varying(255),
    apto_dominial character varying(255),
    geom public.geometry(Point,22175) NOT NULL,
    observaciones text,
    latitud numeric(10,6),
    longitud numeric(10,6),
    dpto character(2),
    circ character(3),
    secc character(2),
    ch character(4),
    qta character(4),
    fracc character(4),
    mz character(4),
    parc character(5),
    "Nomencl" text
);


--
-- Name: pre_adjudicatario_dispersa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pre_adjudicatario_dispersa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pre_adjudicatario_dispersa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pre_adjudicatario_dispersa_id_seq OWNED BY public.pre_adjudicatario_dispersa.id;


--
-- Name: programa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programa (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    origen character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    fiinancia character varying(200)
);


--
-- Name: programa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programa_id_seq OWNED BY public.programa.id;


--
-- Name: regularizacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.regularizacion (
    id integer NOT NULL,
    expediente character varying(255) NOT NULL,
    fecha_ingreso date NOT NULL,
    apenom character varying(255) NOT NULL,
    documento character varying(255),
    telefono character varying,
    nomenclatura character varying(255),
    localizacion boolean,
    dominio boolean,
    propietario character varying(255),
    plano_mensura character varying(255),
    mensura boolean,
    inscripcion character varying(255),
    regularizable boolean,
    tierras boolean,
    recupero boolean,
    crediticia boolean,
    notificacion_solicitante date,
    geom public.geometry(Polygon,22175) NOT NULL
);


--
-- Name: regularizacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.regularizacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: regularizacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.regularizacion_id_seq OWNED BY public.regularizacion.id;


--
-- Name: resolucion_costos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.resolucion_costos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: resolucion_costos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resolucion_costos (
    id integer DEFAULT nextval('public.resolucion_costos_id_seq'::regclass) NOT NULL,
    nro_largo integer NOT NULL,
    ano integer NOT NULL,
    tipo public.resolucion_costos_tipo NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    nro_corto integer NOT NULL
);


--
-- Name: tierra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tierra (
    id integer NOT NULL,
    tipo public.tierra_tipo NOT NULL,
    tipo_oferente public.tierra_tipo_oferente NOT NULL,
    oferente character varying(255),
    propietario character varying(255),
    dpto character(2) NOT NULL,
    circ character(3) NOT NULL,
    secc character(2) NOT NULL,
    ch character(4) NOT NULL,
    qta character(4) NOT NULL,
    fracc character(4) NOT NULL,
    mz character(4) NOT NULL,
    parc character(5) NOT NULL,
    localidad integer,
    tipo_inscripcion public.tierra_tipo_inscripcion,
    inscripcion character varying(255),
    tipo_doc_probatoria integer,
    apto_fisico boolean,
    apto_dominial boolean,
    apto_localizacion boolean,
    visita_campo boolean,
    visita_profesional character varying(255),
    visita_fecha date,
    localizacion public.tierra_localizacion,
    superficie public.tierra_superficie,
    proyecto_loteo boolean,
    estado public.tierra_estado_ocupacion,
    destino integer,
    otro_destino character varying(255),
    geom public.geometry(Polygon,22175) NOT NULL,
    inundabilidad_solicitado character varying(255),
    inundabilidad_respuesta character varying(255),
    inundabilidad_resolucion character varying(255),
    inundabilidad_observaciones character varying(255),
    dominio_solicitado character varying(255),
    dominio_respuesta character varying(255),
    dominio_observaciones character varying(255),
    municipal_solicitado character varying(255),
    municipal_respuesta character varying(255),
    municipal_observaciones character varying(255),
    tasaciones_solicitado character varying(255),
    tasaciones_respuesta character varying(255),
    tasaciones_observaciones character varying(255),
    tasaciones_valor numeric(10,2),
    lyt_solicitado character varying(255),
    lyt_respuesta character varying(255),
    lyt_observaciones character varying(255),
    proy_solicitado character varying(255),
    proy_respuesta character varying(255),
    proy_observaciones character varying(255),
    social_solicitado character varying(255),
    social_respuesta character varying(255),
    social_observaciones character varying(255),
    informe_solicitado character varying(255),
    informe_respuesta character varying(255),
    informe_observaciones character varying(255),
    infraestructura_solicitado character varying(255),
    infraestructura_respuesta character varying(255),
    infraestructura_observaciones character varying(255),
    updated_by character varying(255),
    updated_at timestamp without time zone,
    observaciones text
);


--
-- Name: tierra_destino; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tierra_destino (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tierra_destino_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tierra_destino_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tierra_destino_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tierra_destino_id_seq OWNED BY public.tierra_destino.id;


--
-- Name: tierra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tierra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tierra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tierra_id_seq OWNED BY public.tierra.id;


--
-- Name: tipo_contratacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_contratacion (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tipo_contratacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_contratacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_contratacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_contratacion_id_seq OWNED BY public.tipo_contratacion.id;


--
-- Name: tipo_doc_probatoria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_doc_probatoria (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tipo_doc_probatoria_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_doc_probatoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_doc_probatoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_doc_probatoria_id_seq OWNED BY public.tipo_doc_probatoria.id;


--
-- Name: tipo_ejecutor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_ejecutor (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tipo_ejecutor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_ejecutor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_ejecutor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_ejecutor_id_seq OWNED BY public.tipo_ejecutor.id;


--
-- Name: tipo_estado; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_estado (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tipo_estado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_estado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_estado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_estado_id_seq OWNED BY public.tipo_estado.id;


--
-- Name: tipo_gestion_tierra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_gestion_tierra (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL
);


--
-- Name: tipo_gestion_tierra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_gestion_tierra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_gestion_tierra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_gestion_tierra_id_seq OWNED BY public.tipo_gestion_tierra.id;


--
-- Name: tipo_infraestructura; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_infraestructura (
);


--
-- Name: tipo_intervencion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_intervencion (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone
);


--
-- Name: tipo_intervencion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_intervencion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_intervencion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_intervencion_id_seq OWNED BY public.tipo_intervencion.id;


--
-- Name: tipo_uf; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipo_uf (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL
);


--
-- Name: tipo_uf_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipo_uf_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipo_uf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipo_uf_id_seq OWNED BY public.tipo_uf.id;


--
-- Name: tmp_regularizacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tmp_regularizacion (
    nro_adjudicatario integer NOT NULL,
    estado character varying(255) NOT NULL
);


--
-- Name: uf; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.uf (
    id integer NOT NULL,
    id_parcela integer NOT NULL,
    uf character varying(10) NOT NULL,
    coefuf numeric(10,5),
    poligono character varying(255),
    observaciones character varying(255),
    geom public.geometry(Polygon,22175),
    updated_by character varying(255),
    updated_at timestamp without time zone,
    res_costos integer,
    tipo integer NOT NULL,
    designacion character varying(255),
    irregular boolean DEFAULT false NOT NULL,
    estado_dominial public.parcela_estado_dominial_2,
    nro_adjudicatario bigint,
    tipo_id_adjudicatario public.tipo_id_adjudicatario,
    fr_mat character varying(255),
    nivel integer
);


--
-- Name: uf_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.uf_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: uf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.uf_id_seq OWNED BY public.uf.id;


--
-- Name: vivienda_punto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vivienda_punto (
    id integer NOT NULL,
    id_intervencion integer NOT NULL,
    nomenclatura character(28),
    dpto character(2),
    circ character(3),
    secc character(2),
    ch character(4),
    qta character(4),
    fracc character(4),
    mz character(4),
    parc character(5),
    estado_dominial public.parcela_estado_dominial NOT NULL,
    geom public.geometry(Point,22175) NOT NULL,
    updated_by character varying(255),
    updated_at timestamp without time zone,
    res_costos integer,
    nro_adjudicatario bigint,
    tipo_id_adjudicatario public.tipo_id_adjudicatario,
    nombre character varying(255),
    apellido character varying(255)
);


--
-- Name: vivienda_punto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vivienda_punto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vivienda_punto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vivienda_punto_id_seq OWNED BY public.vivienda_punto.id;


--
-- Name: zonas_parcelas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.zonas_parcelas (
    gid integer NOT NULL,
    nombre character varying(254),
    geom public.geometry(MultiPolygon,22175)
);


--
-- Name: zonas_parcelas_gid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.zonas_parcelas_gid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: zonas_parcelas_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.zonas_parcelas_gid_seq OWNED BY public.zonas_parcelas.gid;


--
-- Name: viviendas; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.viviendas AS
 SELECT p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    i.drf_plan AS plan,
    i.drf_grupo AS grupo,
    ti.nombre AS tipo_obra,
    l.localidad,
    parc.dpto,
    parc.circ,
    parc.secc,
    parc.ch,
    parc.qta,
    parc.fracc,
    parc.mz,
    parc.parc,
    uf.poligono AS uf,
    tu.nombre AS tipo_uf,
    uf.estado_dominial,
    uf.nro_adjudicatario,
    uf.tipo_id_adjudicatario,
    uf.fr_mat,
    (((((ab.nro)::text || '/'::text) || ab.ano) || ' - '::text) || ab.tipo) AS adjudicacion,
    ((((rc.nro_largo || '/'::text) || rc.ano) || ' - '::text) || rc.tipo) AS res_costos,
    uf.geom,
    uf.id,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos
   FROM ((((((((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.parcela parc ON ((i.id = parc.id_intervencion)))
     JOIN public.destino_parcela dp ON ((parc.destino = dp.id)))
     JOIN public.uf ON ((uf.id_parcela = parc.id)))
     JOIN public.tipo_uf tu ON ((tu.id = uf.tipo)))
     LEFT JOIN public.adjudicacion_beneficiario ab ON ((ab.id = i.id_adjudicacion)))
     LEFT JOIN public.resolucion_costos rc ON ((rc.id = uf.res_costos)));


--
-- Name: area; Type: TABLE; Schema: visualizador; Owner: -
--

CREATE TABLE visualizador.area (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL
);


--
-- Name: area_id_seq; Type: SEQUENCE; Schema: visualizador; Owner: -
--

CREATE SEQUENCE visualizador.area_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: area_id_seq; Type: SEQUENCE OWNED BY; Schema: visualizador; Owner: -
--

ALTER SEQUENCE visualizador.area_id_seq OWNED BY visualizador.area.id;


--
-- Name: barrios; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.barrios AS
 SELECT p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    ti.nombre AS tipo_obra,
    l.localidad,
    b.nombre AS barrio,
    b.geom,
    b.id,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos
   FROM (((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.barrio b ON ((i.id = b.id_intervencion)));


--
-- Name: calles; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.calles AS
 SELECT p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    ti.nombre AS tipo_obra,
    l.localidad,
    calle.nombre AS calle,
    calle.geom,
    calle.id,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos
   FROM (((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.calle ON ((i.id = calle.id_intervencion)));


--
-- Name: expropiaciones; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.expropiaciones AS
 SELECT ((((e.nro_ley)::text || (COALESCE(e.letra_ley, ''::bpchar))::text) || '/'::text) || (COALESCE(e.ano_ley, 0))::text) AS ley,
    l.localidad,
    p.dpto,
    p.circ,
    p.secc,
    p.ch,
    p.qta,
    p.fracc,
    p.mz,
    p.parc,
    p.inscripcion AS folio,
    o.nombre AS objeto,
    p.propietario_actual AS propietario_expropiado,
    eg.nombre AS estado,
    p.geom,
    p.id,
    e.gestion
   FROM ((((public.expropiacion e
     JOIN public.parcela_expropiada p ON ((e.id = p.id_expropiacion)))
     JOIN public.objeto_expropiacion o ON ((o.id = p.objeto)))
     JOIN public.estado_gestion_expropiacion eg ON ((eg.id = p.estado_gestion)))
     JOIN public.localidad l ON ((l.id = e.localidad)));


--
-- Name: manzanas; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.manzanas AS
 SELECT p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    ti.nombre AS tipo_obra,
    l.localidad,
    m.nombre AS manzana,
    m.geom,
    m.id,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos
   FROM (((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.manzana m ON ((i.id = m.id_intervencion)));


--
-- Name: ph; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.ph AS
SELECT
    NULL::integer AS id,
    NULL::character varying(255) AS programa,
    NULL::character varying(255) AS actuacion,
    NULL::character varying(255) AS instrumento,
    NULL::integer AS ano,
    NULL::character varying(255) AS expediente,
    NULL::character varying(255) AS contratacion,
    NULL::character varying(255) AS tipo_contratacion,
    NULL::character varying(255) AS obra,
    NULL::integer AS plan,
    NULL::integer AS grupo,
    NULL::character varying(255) AS tipo_obra,
    NULL::character varying(255) AS localidad,
    NULL::character(2) AS dpto,
    NULL::character(3) AS circ,
    NULL::character(2) AS secc,
    NULL::character(4) AS ch,
    NULL::character(4) AS qta,
    NULL::character(4) AS fracc,
    NULL::character(4) AS mz,
    NULL::character(5) AS parc,
    NULL::public.geometry(Polygon,22175) AS geom,
    NULL::bigint AS ufs;


--
-- Name: role; Type: TABLE; Schema: visualizador; Owner: -
--

CREATE TABLE visualizador.role (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text NOT NULL,
    "group" integer NOT NULL,
    objeto character varying(255) DEFAULT 'nada'::character varying NOT NULL,
    permiso character varying(255) DEFAULT 'nada'::character varying NOT NULL
);


--
-- Name: role_id_seq; Type: SEQUENCE; Schema: visualizador; Owner: -
--

CREATE SEQUENCE visualizador.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: visualizador; Owner: -
--

ALTER SEQUENCE visualizador.role_id_seq OWNED BY visualizador.role.id;


--
-- Name: rolegroup; Type: TABLE; Schema: visualizador; Owner: -
--

CREATE TABLE visualizador.rolegroup (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text NOT NULL
);


--
-- Name: rolegroup_id_seq; Type: SEQUENCE; Schema: visualizador; Owner: -
--

CREATE SEQUENCE visualizador.rolegroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rolegroup_id_seq; Type: SEQUENCE OWNED BY; Schema: visualizador; Owner: -
--

ALTER SEQUENCE visualizador.rolegroup_id_seq OWNED BY visualizador.rolegroup.id;


--
-- Name: rolemapping; Type: TABLE; Schema: visualizador; Owner: -
--

CREATE TABLE visualizador.rolemapping (
    id integer NOT NULL,
    "user" integer NOT NULL,
    role integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer
);


--
-- Name: rolemapping_id_seq; Type: SEQUENCE; Schema: visualizador; Owner: -
--

CREATE SEQUENCE visualizador.rolemapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rolemapping_id_seq; Type: SEQUENCE OWNED BY; Schema: visualizador; Owner: -
--

ALTER SEQUENCE visualizador.rolemapping_id_seq OWNED BY visualizador.rolemapping.id;


--
-- Name: user; Type: TABLE; Schema: visualizador; Owner: -
--

CREATE TABLE visualizador."user" (
    id integer NOT NULL,
    nombre character varying(255),
    username character varying(255),
    password character varying(255) NOT NULL,
    token character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    email character varying(255),
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer,
    activo boolean DEFAULT true NOT NULL,
    area integer,
    tokenm character varying(255)
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: visualizador; Owner: -
--

CREATE SEQUENCE visualizador.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: visualizador; Owner: -
--

ALTER SEQUENCE visualizador.user_id_seq OWNED BY visualizador."user".id;


--
-- Name: vivienda_dispersa; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.vivienda_dispersa AS
 SELECT p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    i.drf_plan AS plan,
    i.drf_grupo AS grupo,
    ti.nombre AS tipo_obra,
    l.localidad,
    vp.dpto,
    vp.circ,
    vp.secc,
    vp.ch,
    vp.qta,
    vp.fracc,
    vp.mz,
    vp.parc,
    (((((ab.nro)::text || '/'::text) || ab.ano) || ' - '::text) || ab.tipo) AS adjudicacion,
    ((((rc.nro_largo || '/'::text) || rc.ano) || ' - '::text) || rc.tipo) AS res_costos,
    vp.geom,
    (public.st_y(public.st_transform(vp.geom, 4326)))::numeric(10,6) AS latitud,
    (public.st_x(public.st_transform(vp.geom, 4326)))::numeric(10,6) AS longitud,
    vp.id,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos
   FROM (((((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.vivienda_punto vp ON ((i.id = vp.id_intervencion)))
     LEFT JOIN public.adjudicacion_beneficiario ab ON ((ab.id = i.id_adjudicacion)))
     LEFT JOIN public.resolucion_costos rc ON ((rc.id = vp.res_costos)));


--
-- Name: viviendas_ph; Type: VIEW; Schema: visualizador; Owner: -
--

CREATE VIEW visualizador.viviendas_ph AS
 SELECT uf.id,
    p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    i.drf_plan AS plan,
    i.drf_grupo AS grupo,
    ti.nombre AS tipo_obra,
    l.localidad,
    parc.id AS id_parcela,
    parc.dpto,
    parc.circ,
    parc.secc,
    parc.ch,
    parc.qta,
    parc.fracc,
    parc.mz,
    parc.parc,
    uf.uf,
    uf.coefuf,
    uf.observaciones,
    uf.designacion,
    uf.poligono,
    tu.nombre AS tipo_uf,
    uf.estado_dominial,
    uf.nro_adjudicatario,
    uf.tipo_id_adjudicatario,
    uf.fr_mat,
    (((((ab.nro)::text || '/'::text) || ab.ano) || ' - '::text) || ab.tipo) AS adjudicacion,
    ((((rc.nro_largo || '/'::text) || rc.ano) || ' - '::text) || rc.tipo) AS res_costos,
    adj."AdjuGISapeynom" AS adjudicatario3450,
    adj."AdjuGISEscritura" AS escritura3450,
    adj."AdjuGISsituacion" AS situacion3450,
    adj."AdjuGISmotivo" AS motivo3450,
    adj."AdjuGISmatricula" AS matricula3450,
    uf.geom,
    array_to_string(ARRAY( SELECT e.nombre
           FROM (public.intervencion_ejecutor ie
             JOIN public.ejecutor e ON ((ie.id_ejecutor = e.id)))
          WHERE (ie.id_intervencion = i.id)), ', '::text) AS ejecutores,
    array_to_string(ARRAY( SELECT ((((((((pm.depto)::text || '-'::text) || pm.nro) || '-'::text) || (pm.ano)::text) || '/'::text) || pmi.tipo))::character varying AS "varchar"
           FROM (public.plano_mensura_intervencion pmi
             JOIN public.plano_mensura pm ON ((pm.id = pmi.idplano)))
          WHERE (pmi.idintervencion = i.id)), ', '::text) AS planos,
    uf.nivel
   FROM (((((((((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.parcela parc ON ((i.id = parc.id_intervencion)))
     JOIN public.destino_parcela dp ON ((parc.destino = dp.id)))
     JOIN public.uf ON ((uf.id_parcela = parc.id)))
     JOIN public.tipo_uf tu ON ((tu.id = uf.tipo)))
     LEFT JOIN public.adjudicacion_beneficiario ab ON ((ab.id = i.id_adjudicacion)))
     LEFT JOIN public.resolucion_costos rc ON ((rc.id = uf.res_costos)))
     LEFT JOIN public.adjudicatario3450 adj ON ((uf.nro_adjudicatario = adj."AdjuGISNroAdju")))
  WHERE (parc.es_ph = true)
  ORDER BY parc.id, uf.uf;


--
-- Name: audit_logs id; Type: DEFAULT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.audit_logs ALTER COLUMN id SET DEFAULT nextval('audit.audit_logs_id_seq'::regclass);


--
-- Name: encuesta id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.encuesta ALTER COLUMN id SET DEFAULT nextval('our.encuesta_id_seq'::regclass);


--
-- Name: pregunta id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta ALTER COLUMN id SET DEFAULT nextval('our.pregunta_id_seq'::regclass);


--
-- Name: pregunta_relevamiento id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento ALTER COLUMN id SET DEFAULT nextval('our.pregunta_relevamiento_id_seq'::regclass);


--
-- Name: relevamiento id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.relevamiento ALTER COLUMN id SET DEFAULT nextval('our.relevamiento_id_seq'::regclass);


--
-- Name: respuesta id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta ALTER COLUMN id SET DEFAULT nextval('our.respuesta_id_seq'::regclass);


--
-- Name: respuesta_encuesta id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta_encuesta ALTER COLUMN id SET DEFAULT nextval('our.respuesta_encuesta_id_seq'::regclass);


--
-- Name: seccion id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.seccion ALTER COLUMN id SET DEFAULT nextval('our.seccion_id_seq'::regclass);


--
-- Name: tipo_pregunta id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.tipo_pregunta ALTER COLUMN id SET DEFAULT nextval('our.tipo_pregunta_id_seq'::regclass);


--
-- Name: vivienda id; Type: DEFAULT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.vivienda ALTER COLUMN id SET DEFAULT nextval('our.vivienda_id_seq'::regclass);


--
-- Name: actuacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.actuacion ALTER COLUMN id SET DEFAULT nextval('public.actuacion_id_seq'::regclass);


--
-- Name: adjudicacion_beneficiario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adjudicacion_beneficiario ALTER COLUMN id SET DEFAULT nextval('public.adjudicacion_beneficiario_id_seq'::regclass);


--
-- Name: barrio id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.barrio ALTER COLUMN id SET DEFAULT nextval('public.barrio_id_seq'::regclass);


--
-- Name: calle id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calle ALTER COLUMN id SET DEFAULT nextval('public.calle_id_seq'::regclass);


--
-- Name: catastrourbano id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.catastrourbano ALTER COLUMN id SET DEFAULT nextval('public.catastrourbano_gid_seq'::regclass);


--
-- Name: contratacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratacion ALTER COLUMN id SET DEFAULT nextval('public.contratacion_id_seq'::regclass);


--
-- Name: departamento gid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamento ALTER COLUMN gid SET DEFAULT nextval('public.departamento_gid_seq'::regclass);


--
-- Name: destino_parcela id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destino_parcela ALTER COLUMN id SET DEFAULT nextval('public.destino_parcela_id_seq'::regclass);


--
-- Name: ejecutor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ejecutor ALTER COLUMN id SET DEFAULT nextval('public.ejecutor_id_seq'::regclass);


--
-- Name: estado_dominial id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_dominial ALTER COLUMN id SET DEFAULT nextval('public.estado_dominial_id_seq'::regclass);


--
-- Name: estado_gestion_expropiacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_gestion_expropiacion ALTER COLUMN id SET DEFAULT nextval('public.estado_gestion_expropiacion_id_seq'::regclass);


--
-- Name: inspector id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inspector ALTER COLUMN id SET DEFAULT nextval('public.inspector_id_seq'::regclass);


--
-- Name: intervencion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion ALTER COLUMN id SET DEFAULT nextval('public.intervencion_id_seq'::regclass);


--
-- Name: intervencion_ejecutor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_ejecutor ALTER COLUMN id SET DEFAULT nextval('public.intervencion_ejecutor_id_seq'::regclass);


--
-- Name: intervencion_inspector id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_inspector ALTER COLUMN id SET DEFAULT nextval('public.intervencion_inspector_id_seq'::regclass);


--
-- Name: layer_styles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.layer_styles ALTER COLUMN id SET DEFAULT nextval('public.layer_styles_id_seq'::regclass);


--
-- Name: localidad id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.localidad ALTER COLUMN id SET DEFAULT nextval('public.localidad_id_seq'::regclass);


--
-- Name: manzana id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manzana ALTER COLUMN id SET DEFAULT nextval('public.manzana_id_seq'::regclass);


--
-- Name: objeto_expropiacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.objeto_expropiacion ALTER COLUMN id SET DEFAULT nextval('public.objeto_expropiacion_id_seq'::regclass);


--
-- Name: parcela id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela ALTER COLUMN id SET DEFAULT nextval('public.parcela_id_seq'::regclass);


--
-- Name: plano_mensura id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura ALTER COLUMN id SET DEFAULT nextval('public.plano_mensura_id_seq'::regclass);


--
-- Name: plano_mensura_intervencion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_intervencion ALTER COLUMN id SET DEFAULT nextval('public.plano_mensura_intervencion_id_seq'::regclass);


--
-- Name: plano_mensura_tierra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_tierra ALTER COLUMN id SET DEFAULT nextval('public.plano_mensura_tierra_id_seq'::regclass);


--
-- Name: pre_adjudicatario_dispersa id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pre_adjudicatario_dispersa ALTER COLUMN id SET DEFAULT nextval('public.pre_adjudicatario_dispersa_id_seq'::regclass);


--
-- Name: programa id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programa ALTER COLUMN id SET DEFAULT nextval('public.programa_id_seq'::regclass);


--
-- Name: regularizacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.regularizacion ALTER COLUMN id SET DEFAULT nextval('public.regularizacion_id_seq'::regclass);


--
-- Name: tierra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra ALTER COLUMN id SET DEFAULT nextval('public.tierra_id_seq'::regclass);


--
-- Name: tierra_destino id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra_destino ALTER COLUMN id SET DEFAULT nextval('public.tierra_destino_id_seq'::regclass);


--
-- Name: tipo_contratacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_contratacion ALTER COLUMN id SET DEFAULT nextval('public.tipo_contratacion_id_seq'::regclass);


--
-- Name: tipo_doc_probatoria id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_doc_probatoria ALTER COLUMN id SET DEFAULT nextval('public.tipo_doc_probatoria_id_seq'::regclass);


--
-- Name: tipo_ejecutor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_ejecutor ALTER COLUMN id SET DEFAULT nextval('public.tipo_ejecutor_id_seq'::regclass);


--
-- Name: tipo_estado id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_estado ALTER COLUMN id SET DEFAULT nextval('public.tipo_estado_id_seq'::regclass);


--
-- Name: tipo_gestion_tierra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_gestion_tierra ALTER COLUMN id SET DEFAULT nextval('public.tipo_gestion_tierra_id_seq'::regclass);


--
-- Name: tipo_intervencion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_intervencion ALTER COLUMN id SET DEFAULT nextval('public.tipo_intervencion_id_seq'::regclass);


--
-- Name: tipo_uf id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_uf ALTER COLUMN id SET DEFAULT nextval('public.tipo_uf_id_seq'::regclass);


--
-- Name: uf id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uf ALTER COLUMN id SET DEFAULT nextval('public.uf_id_seq'::regclass);


--
-- Name: vivienda_punto id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vivienda_punto ALTER COLUMN id SET DEFAULT nextval('public.vivienda_punto_id_seq'::regclass);


--
-- Name: zonas_parcelas gid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zonas_parcelas ALTER COLUMN gid SET DEFAULT nextval('public.zonas_parcelas_gid_seq'::regclass);


--
-- Name: area id; Type: DEFAULT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.area ALTER COLUMN id SET DEFAULT nextval('visualizador.area_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.role ALTER COLUMN id SET DEFAULT nextval('visualizador.role_id_seq'::regclass);


--
-- Name: rolegroup id; Type: DEFAULT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolegroup ALTER COLUMN id SET DEFAULT nextval('visualizador.rolegroup_id_seq'::regclass);


--
-- Name: rolemapping id; Type: DEFAULT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping ALTER COLUMN id SET DEFAULT nextval('visualizador.rolemapping_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador."user" ALTER COLUMN id SET DEFAULT nextval('visualizador.user_id_seq'::regclass);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: encuesta encuesta_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.encuesta
    ADD CONSTRAINT encuesta_pkey PRIMARY KEY (id);


--
-- Name: pregunta pregunta_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta
    ADD CONSTRAINT pregunta_pkey PRIMARY KEY (id);


--
-- Name: pregunta_relevamiento pregunta_relevamiento_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento
    ADD CONSTRAINT pregunta_relevamiento_pkey PRIMARY KEY (id);


--
-- Name: pregunta_relevamiento rel_variable_unique; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento
    ADD CONSTRAINT rel_variable_unique UNIQUE (relevamiento, variable) INCLUDE (relevamiento, variable);


--
-- Name: relevamiento relevamiento_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.relevamiento
    ADD CONSTRAINT relevamiento_pkey PRIMARY KEY (id);


--
-- Name: respuesta_encuesta respuesta_encuesta_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta_encuesta
    ADD CONSTRAINT respuesta_encuesta_pkey PRIMARY KEY (id);


--
-- Name: respuesta respuesta_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta
    ADD CONSTRAINT respuesta_pkey PRIMARY KEY (id);


--
-- Name: respuesta respuesta_pregunta_nro_opcion_key; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta
    ADD CONSTRAINT respuesta_pregunta_nro_opcion_key UNIQUE (pregunta, nro_opcion);


--
-- Name: seccion seccion_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.seccion
    ADD CONSTRAINT seccion_pkey PRIMARY KEY (id);


--
-- Name: tipo_pregunta tipo_pregunta_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.tipo_pregunta
    ADD CONSTRAINT tipo_pregunta_pkey PRIMARY KEY (id);


--
-- Name: vivienda vivienda_pkey; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.vivienda
    ADD CONSTRAINT vivienda_pkey PRIMARY KEY (id);


--
-- Name: vivienda vivienda_relevamiento_vivienda_relevamiento1_vivienda1_key; Type: CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.vivienda
    ADD CONSTRAINT vivienda_relevamiento_vivienda_relevamiento1_vivienda1_key UNIQUE (relevamiento, vivienda) INCLUDE (relevamiento, vivienda);


--
-- Name: actuacion actuacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.actuacion
    ADD CONSTRAINT actuacion_pkey PRIMARY KEY (id);


--
-- Name: adjudicacion_beneficiario adjudicacion_beneficiario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adjudicacion_beneficiario
    ADD CONSTRAINT adjudicacion_beneficiario_pkey PRIMARY KEY (id);


--
-- Name: adjudicatario3450 adjudicatario3450_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adjudicatario3450
    ADD CONSTRAINT adjudicatario3450_pkey PRIMARY KEY ("AdjuGISNroAdju");


--
-- Name: barrio barrio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.barrio
    ADD CONSTRAINT barrio_pkey PRIMARY KEY (id);


--
-- Name: calle calle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calle
    ADD CONSTRAINT calle_pkey PRIMARY KEY (id);


--
-- Name: catastrourbano catastrourbano_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.catastrourbano
    ADD CONSTRAINT catastrourbano_pkey PRIMARY KEY (id);


--
-- Name: contratacion contratacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratacion
    ADD CONSTRAINT contratacion_pkey PRIMARY KEY (id);


--
-- Name: departamento departamento_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamento
    ADD CONSTRAINT departamento_pkey PRIMARY KEY (gid);


--
-- Name: destino_parcela destino_parcela_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.destino_parcela
    ADD CONSTRAINT destino_parcela_pkey PRIMARY KEY (id);


--
-- Name: ejecutor ejecutor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ejecutor
    ADD CONSTRAINT ejecutor_pkey PRIMARY KEY (id);


--
-- Name: expropiacion expropiacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.expropiacion
    ADD CONSTRAINT expropiacion_pkey PRIMARY KEY (id);


--
-- Name: inspector inspector_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inspector
    ADD CONSTRAINT inspector_pkey PRIMARY KEY (id);


--
-- Name: intervencion_ejecutor intervencion_ejecutor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_ejecutor
    ADD CONSTRAINT intervencion_ejecutor_pkey PRIMARY KEY (id);


--
-- Name: intervencion_inspector intervencion_inspector_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_inspector
    ADD CONSTRAINT intervencion_inspector_pkey PRIMARY KEY (id);


--
-- Name: intervencion intervencion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_pkey PRIMARY KEY (id);


--
-- Name: layer_styles layer_styles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.layer_styles
    ADD CONSTRAINT layer_styles_pkey PRIMARY KEY (id);


--
-- Name: localidad localidad_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.localidad
    ADD CONSTRAINT localidad_pkey PRIMARY KEY (id);


--
-- Name: manzana manzana_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manzana
    ADD CONSTRAINT manzana_pkey PRIMARY KEY (id);


--
-- Name: municipio municipio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipio
    ADD CONSTRAINT municipio_pkey PRIMARY KEY (id);


--
-- Name: objeto_expropiacion objeto_expropiacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.objeto_expropiacion
    ADD CONSTRAINT objeto_expropiacion_pkey PRIMARY KEY (id);


--
-- Name: parcela_expropiada parcela_expropiada_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela_expropiada
    ADD CONSTRAINT parcela_expropiada_pkey PRIMARY KEY (id);


--
-- Name: parcela parcela_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela
    ADD CONSTRAINT parcela_pkey PRIMARY KEY (id);


--
-- Name: plano_mensura_intervencion plano_mensura_intervencion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_intervencion
    ADD CONSTRAINT plano_mensura_intervencion_pkey PRIMARY KEY (id);


--
-- Name: plano_mensura plano_mensura_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura
    ADD CONSTRAINT plano_mensura_pkey PRIMARY KEY (id);


--
-- Name: plano_mensura_tierra plano_mensura_tierra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_tierra
    ADD CONSTRAINT plano_mensura_tierra_pkey PRIMARY KEY (id);


--
-- Name: pre_adjudicatario_dispersa pre_adjudicatario_dispersa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pre_adjudicatario_dispersa
    ADD CONSTRAINT pre_adjudicatario_dispersa_pkey PRIMARY KEY (id);


--
-- Name: programa programa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programa
    ADD CONSTRAINT programa_pkey PRIMARY KEY (id);


--
-- Name: regularizacion regularizacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.regularizacion
    ADD CONSTRAINT regularizacion_pkey PRIMARY KEY (id);


--
-- Name: resolucion_costos resolucion_costos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolucion_costos
    ADD CONSTRAINT resolucion_costos_pkey PRIMARY KEY (id);


--
-- Name: estado_gestion_expropiacion sit_dominial_expropiacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estado_gestion_expropiacion
    ADD CONSTRAINT sit_dominial_expropiacion_pkey PRIMARY KEY (id);


--
-- Name: tierra_destino tierra_destino_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra_destino
    ADD CONSTRAINT tierra_destino_pkey PRIMARY KEY (id);


--
-- Name: tierra tierra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra
    ADD CONSTRAINT tierra_pkey PRIMARY KEY (id);


--
-- Name: tipo_contratacion tipo_contratacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_contratacion
    ADD CONSTRAINT tipo_contratacion_pkey PRIMARY KEY (id);


--
-- Name: tipo_doc_probatoria tipo_doc_probatoria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_doc_probatoria
    ADD CONSTRAINT tipo_doc_probatoria_pkey PRIMARY KEY (id);


--
-- Name: tipo_ejecutor tipo_ejecutor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_ejecutor
    ADD CONSTRAINT tipo_ejecutor_pkey PRIMARY KEY (id);


--
-- Name: tipo_estado tipo_estado_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_estado
    ADD CONSTRAINT tipo_estado_pkey PRIMARY KEY (id);


--
-- Name: tipo_gestion_tierra tipo_gestion_tierra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_gestion_tierra
    ADD CONSTRAINT tipo_gestion_tierra_pkey PRIMARY KEY (id);


--
-- Name: tipo_intervencion tipo_intervencion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_intervencion
    ADD CONSTRAINT tipo_intervencion_pkey PRIMARY KEY (id);


--
-- Name: tipo_uf tipo_uf_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipo_uf
    ADD CONSTRAINT tipo_uf_pkey PRIMARY KEY (id);


--
-- Name: tmp_regularizacion tmp_regularizacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tmp_regularizacion
    ADD CONSTRAINT tmp_regularizacion_pkey PRIMARY KEY (nro_adjudicatario);


--
-- Name: uf uf_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uf
    ADD CONSTRAINT uf_pkey PRIMARY KEY (id);


--
-- Name: vivienda_punto vivienda_punto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vivienda_punto
    ADD CONSTRAINT vivienda_punto_pkey PRIMARY KEY (id);


--
-- Name: zonas_parcelas zonas_parcelas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zonas_parcelas
    ADD CONSTRAINT zonas_parcelas_pkey PRIMARY KEY (gid);


--
-- Name: area area_pkey; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.area
    ADD CONSTRAINT area_pkey PRIMARY KEY (id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: rolegroup rolegroup_pkey; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolegroup
    ADD CONSTRAINT rolegroup_pkey PRIMARY KEY (id);


--
-- Name: rolemapping rolemapping_pkey; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping
    ADD CONSTRAINT rolemapping_pkey PRIMARY KEY (id);


--
-- Name: rolemapping rolemapping_user_role_key; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping
    ADD CONSTRAINT rolemapping_user_role_key UNIQUE ("user", role);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: actuacion_id_programa_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX actuacion_id_programa_idx ON public.actuacion USING btree (id_programa);


--
-- Name: barrio_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX barrio_geom_idx ON public.barrio USING gist (geom);


--
-- Name: barrio_id_intervencion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX barrio_id_intervencion_idx ON public.barrio USING btree (id_intervencion);


--
-- Name: calle_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX calle_geom_idx ON public.calle USING gist (geom);


--
-- Name: calle_id_intervencion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX calle_id_intervencion_idx ON public.calle USING btree (id_intervencion);


--
-- Name: catastrourbano_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX catastrourbano_geom_idx ON public.catastrourbano USING gist (geom);


--
-- Name: contratacion_id_actuacion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contratacion_id_actuacion_idx ON public.contratacion USING btree (id_actuacion);


--
-- Name: contratacion_tipo_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contratacion_tipo_idx ON public.contratacion USING btree (tipo);


--
-- Name: departamento_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX departamento_geom_idx ON public.departamento USING gist (geom);


--
-- Name: ejecutor_id_localidad_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ejecutor_id_localidad_idx ON public.ejecutor USING btree (id_localidad);


--
-- Name: ejecutor_tipo_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ejecutor_tipo_idx ON public.ejecutor USING btree (tipo);


--
-- Name: expropiacion_localidad_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX expropiacion_localidad_idx ON public.expropiacion USING btree (localidad);


--
-- Name: fki_parcela_expropiada_objeto_expropiacion_fk; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_parcela_expropiada_objeto_expropiacion_fk ON public.parcela_expropiada USING btree (objeto);


--
-- Name: id_nomencl_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX id_nomencl_idx ON public.catastrourbano USING btree (id_nomencl) INCLUDE (municipio);


--
-- Name: intervencion_estado_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intervencion_estado_idx ON public.intervencion USING btree (estado);


--
-- Name: intervencion_id_adjudicacion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intervencion_id_adjudicacion_idx ON public.intervencion USING btree (id_adjudicacion);


--
-- Name: intervencion_id_contratacion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intervencion_id_contratacion_idx ON public.intervencion USING btree (id_contratacion);


--
-- Name: intervencion_id_localidad_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intervencion_id_localidad_idx ON public.intervencion USING btree (id_localidad);


--
-- Name: intervencion_tipo_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intervencion_tipo_idx ON public.intervencion USING btree (tipo);


--
-- Name: localidad_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX localidad_geom_idx ON public.localidad USING gist (geom);


--
-- Name: manzana_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX manzana_geom_idx ON public.manzana USING gist (geom);


--
-- Name: manzana_id_intervencion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX manzana_id_intervencion_idx ON public.manzana USING btree (id_intervencion);


--
-- Name: municipio_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX municipio_geom_idx ON public.municipio USING gist (geom);


--
-- Name: parcela_destino_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parcela_destino_idx ON public.parcela USING btree (destino);


--
-- Name: parcela_expropiada_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parcela_expropiada_geom_idx ON public.parcela_expropiada USING gist (geom);


--
-- Name: parcela_expropiada_id_expropiacion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parcela_expropiada_id_expropiacion_idx ON public.parcela_expropiada USING btree (id_expropiacion);


--
-- Name: parcela_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parcela_geom_idx ON public.parcela USING gist (geom);


--
-- Name: parcela_id_intervencion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parcela_id_intervencion_idx ON public.parcela USING btree (id_intervencion);


--
-- Name: tierra_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tierra_geom_idx ON public.tierra USING gist (geom);


--
-- Name: uf_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX uf_geom_idx ON public.uf USING gist (geom);


--
-- Name: uf_id_parcela_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX uf_id_parcela_idx ON public.uf USING btree (id_parcela);


--
-- Name: uf_res_costos_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX uf_res_costos_idx ON public.uf USING btree (res_costos);


--
-- Name: uf_tipo_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX uf_tipo_idx ON public.uf USING btree (tipo);


--
-- Name: vivienda_punto_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vivienda_punto_geom_idx ON public.vivienda_punto USING gist (geom);


--
-- Name: vivienda_punto_id_intervencion_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vivienda_punto_id_intervencion_idx ON public.vivienda_punto USING btree (id_intervencion);


--
-- Name: vivienda_punto_res_costos_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vivienda_punto_res_costos_idx ON public.vivienda_punto USING btree (res_costos);


--
-- Name: zonas_parcelas_geom_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX zonas_parcelas_geom_idx ON public.zonas_parcelas USING gist (geom);


--
-- Name: ph _RETURN; Type: RULE; Schema: visualizador; Owner: -
--

CREATE OR REPLACE VIEW visualizador.ph AS
 SELECT parc.id,
    p.nombre AS programa,
    a.nombre AS actuacion,
    a.instrumento,
    a.ano,
    COALESCE(c.expediente, c.resolucion) AS expediente,
    c.nombre AS contratacion,
    tc.nombre AS tipo_contratacion,
    i.nombre AS obra,
    i.drf_plan AS plan,
    i.drf_grupo AS grupo,
    ti.nombre AS tipo_obra,
    l.localidad,
    parc.dpto,
    parc.circ,
    parc.secc,
    parc.ch,
    parc.qta,
    parc.fracc,
    parc.mz,
    parc.parc,
    parc.geom,
    count(uf.id) AS ufs
   FROM ((((((((public.programa p
     JOIN public.actuacion a ON ((p.id = a.id_programa)))
     JOIN public.contratacion c ON ((a.id = c.id_actuacion)))
     JOIN public.tipo_contratacion tc ON ((tc.id = c.tipo)))
     JOIN public.intervencion i ON ((c.id = i.id_contratacion)))
     JOIN public.localidad l ON ((l.id = i.id_localidad)))
     JOIN public.tipo_intervencion ti ON ((ti.id = i.tipo)))
     JOIN public.parcela parc ON ((i.id = parc.id_intervencion)))
     JOIN public.uf ON ((uf.id_parcela = parc.id)))
  WHERE (parc.es_ph = true)
  GROUP BY parc.id, p.nombre, a.nombre, a.instrumento, a.ano, COALESCE(c.expediente, c.resolucion), c.nombre, tc.nombre, i.nombre, i.drf_plan, i.drf_grupo, ti.nombre, l.localidad;


--
-- Name: encuesta update_vivienda; Type: TRIGGER; Schema: our; Owner: -
--

CREATE TRIGGER update_vivienda AFTER INSERT ON our.encuesta FOR EACH ROW EXECUTE FUNCTION our.update_vivienda_relevado();


--
-- Name: parcela set_nomenclatura; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_nomenclatura BEFORE INSERT OR UPDATE ON public.parcela FOR EACH ROW EXECUTE FUNCTION public.set_nomenclatura();


--
-- Name: parcela_expropiada set_nomenclatura; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_nomenclatura BEFORE INSERT OR UPDATE ON public.parcela_expropiada FOR EACH ROW EXECUTE FUNCTION public.set_nomenclatura();


--
-- Name: vivienda_punto set_nomenclatura; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_nomenclatura BEFORE INSERT OR UPDATE ON public.vivienda_punto FOR EACH ROW EXECUTE FUNCTION public.set_nomenclatura();


--
-- Name: actuacion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.actuacion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: adjudicacion_beneficiario set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.adjudicacion_beneficiario FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: barrio set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.barrio FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: calle set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.calle FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: contratacion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.contratacion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: departamento set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.departamento FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: destino_parcela set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.destino_parcela FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: ejecutor set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.ejecutor FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: expropiacion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.expropiacion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: inspector set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.inspector FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: intervencion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.intervencion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: intervencion_ejecutor set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.intervencion_ejecutor FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: localidad set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.localidad FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: manzana set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.manzana FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: municipio set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.municipio FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: objeto_expropiacion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.objeto_expropiacion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: parcela set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.parcela FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: parcela_expropiada set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.parcela_expropiada FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: plano_mensura set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.plano_mensura FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: programa set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.programa FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: resolucion_costos set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.resolucion_costos FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tierra set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tierra FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tierra_destino set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tierra_destino FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tipo_contratacion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tipo_contratacion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tipo_doc_probatoria set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tipo_doc_probatoria FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tipo_ejecutor set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tipo_ejecutor FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tipo_estado set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tipo_estado FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: tipo_intervencion set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.tipo_intervencion FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: uf set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.uf FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: vivienda_punto set_timestamp; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER set_timestamp BEFORE INSERT OR UPDATE ON public.vivienda_punto FOR EACH ROW EXECUTE FUNCTION public.set_updated();


--
-- Name: pre_adjudicatario_dispersa upd_lonlat; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER upd_lonlat BEFORE INSERT OR UPDATE OF geom ON public.pre_adjudicatario_dispersa FOR EACH ROW EXECUTE FUNCTION public.set_lonlat();


--
-- Name: uf upd_ph_delete; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER upd_ph_delete AFTER DELETE ON public.uf REFERENCING OLD TABLE AS old_table FOR EACH STATEMENT EXECUTE FUNCTION public.set_es_ph();


--
-- Name: uf upd_ph_insert; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER upd_ph_insert AFTER INSERT ON public.uf REFERENCING NEW TABLE AS new_table FOR EACH STATEMENT EXECUTE FUNCTION public.set_es_ph();


--
-- Name: uf upd_ph_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER upd_ph_update AFTER UPDATE ON public.uf REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table FOR EACH STATEMENT EXECUTE FUNCTION public.set_es_ph();


--
-- Name: encuesta encuesta_relevamiento_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.encuesta
    ADD CONSTRAINT encuesta_relevamiento_fkey FOREIGN KEY (relevamiento) REFERENCES our.relevamiento(id) ON UPDATE CASCADE;


--
-- Name: encuesta encuesta_vivienda_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.encuesta
    ADD CONSTRAINT encuesta_vivienda_fkey FOREIGN KEY (vivienda, relevamiento) REFERENCES our.vivienda(vivienda, relevamiento);


--
-- Name: pregunta_relevamiento pregunta_relevamiento_pregunta_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento
    ADD CONSTRAINT pregunta_relevamiento_pregunta_fkey FOREIGN KEY (pregunta) REFERENCES our.pregunta(id) ON UPDATE CASCADE;


--
-- Name: pregunta_relevamiento pregunta_relevamiento_relevamiento_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento
    ADD CONSTRAINT pregunta_relevamiento_relevamiento_fkey FOREIGN KEY (relevamiento) REFERENCES our.relevamiento(id) ON UPDATE CASCADE;


--
-- Name: pregunta_relevamiento pregunta_relevamiento_seccion_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta_relevamiento
    ADD CONSTRAINT pregunta_relevamiento_seccion_fkey FOREIGN KEY (seccion) REFERENCES our.seccion(id) ON UPDATE CASCADE;


--
-- Name: pregunta pregunta_tipo_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.pregunta
    ADD CONSTRAINT pregunta_tipo_fkey FOREIGN KEY (tipo) REFERENCES our.tipo_pregunta(id);


--
-- Name: respuesta_encuesta respuesta_encuesta_encuesta_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta_encuesta
    ADD CONSTRAINT respuesta_encuesta_encuesta_fkey FOREIGN KEY (encuesta) REFERENCES our.encuesta(id) ON UPDATE CASCADE;


--
-- Name: respuesta_encuesta respuesta_encuesta_pregunta_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta_encuesta
    ADD CONSTRAINT respuesta_encuesta_pregunta_fkey FOREIGN KEY (pregunta) REFERENCES our.pregunta_relevamiento(id) ON UPDATE CASCADE;


--
-- Name: respuesta_encuesta respuesta_encuesta_respuesta_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta_encuesta
    ADD CONSTRAINT respuesta_encuesta_respuesta_fkey FOREIGN KEY (respuesta) REFERENCES our.respuesta(id) ON UPDATE CASCADE;


--
-- Name: respuesta respuesta_pregunta_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.respuesta
    ADD CONSTRAINT respuesta_pregunta_fkey FOREIGN KEY (pregunta) REFERENCES our.pregunta(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: seccion seccion_relevamiento_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.seccion
    ADD CONSTRAINT seccion_relevamiento_fkey FOREIGN KEY (relevamiento) REFERENCES our.relevamiento(id);


--
-- Name: vivienda vivienda_relevamiento_fkey; Type: FK CONSTRAINT; Schema: our; Owner: -
--

ALTER TABLE ONLY our.vivienda
    ADD CONSTRAINT vivienda_relevamiento_fkey FOREIGN KEY (relevamiento) REFERENCES our.relevamiento(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: actuacion actuacion_programa_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.actuacion
    ADD CONSTRAINT actuacion_programa_fk FOREIGN KEY (id_programa) REFERENCES public.programa(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: barrio barrio_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.barrio
    ADD CONSTRAINT barrio_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: calle calle_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calle
    ADD CONSTRAINT calle_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: contratacion contratacion_actuacion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratacion
    ADD CONSTRAINT contratacion_actuacion_fk FOREIGN KEY (id_actuacion) REFERENCES public.actuacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: contratacion contratacion_tipo_contratacion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratacion
    ADD CONSTRAINT contratacion_tipo_contratacion_fk FOREIGN KEY (tipo) REFERENCES public.tipo_contratacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: ejecutor ejecutor_localidad_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ejecutor
    ADD CONSTRAINT ejecutor_localidad_fk FOREIGN KEY (id_localidad) REFERENCES public.localidad(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: ejecutor ejecutor_tipo_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ejecutor
    ADD CONSTRAINT ejecutor_tipo_fk FOREIGN KEY (tipo) REFERENCES public.tipo_ejecutor(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: expropiacion expropiacion_localidad_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.expropiacion
    ADD CONSTRAINT expropiacion_localidad_fk FOREIGN KEY (localidad) REFERENCES public.localidad(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion intervencion_contratacion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_contratacion_fk FOREIGN KEY (id_contratacion) REFERENCES public.contratacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion_ejecutor intervencion_ejecutor_ejecutor_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_ejecutor
    ADD CONSTRAINT intervencion_ejecutor_ejecutor_fk FOREIGN KEY (id_ejecutor) REFERENCES public.ejecutor(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion_ejecutor intervencion_ejecutor_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_ejecutor
    ADD CONSTRAINT intervencion_ejecutor_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion intervencion_estado_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_estado_fk FOREIGN KEY (estado) REFERENCES public.tipo_estado(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion intervencion_id_adjudicacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_id_adjudicacion_fkey FOREIGN KEY (id_adjudicacion) REFERENCES public.adjudicacion_beneficiario(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: intervencion_inspector intervencion_inspector_idinspector_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_inspector
    ADD CONSTRAINT intervencion_inspector_idinspector_fkey FOREIGN KEY (idinspector) REFERENCES public.inspector(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: intervencion_inspector intervencion_inspector_idintervencion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion_inspector
    ADD CONSTRAINT intervencion_inspector_idintervencion_fkey FOREIGN KEY (idintervencion) REFERENCES public.intervencion(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: intervencion intervencion_localidad_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_localidad_fk FOREIGN KEY (id_localidad) REFERENCES public.localidad(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: intervencion intervencion_tipo_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intervencion
    ADD CONSTRAINT intervencion_tipo_fk FOREIGN KEY (tipo) REFERENCES public.tipo_intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: manzana manzana_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manzana
    ADD CONSTRAINT manzana_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: parcela parcela_destino_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela
    ADD CONSTRAINT parcela_destino_fk FOREIGN KEY (destino) REFERENCES public.destino_parcela(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: parcela_expropiada parcela_expropiada_estado_gestion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela_expropiada
    ADD CONSTRAINT parcela_expropiada_estado_gestion_fkey FOREIGN KEY (estado_gestion) REFERENCES public.estado_gestion_expropiacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: parcela_expropiada parcela_expropiada_expropiacion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela_expropiada
    ADD CONSTRAINT parcela_expropiada_expropiacion_fk FOREIGN KEY (id_expropiacion) REFERENCES public.expropiacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: parcela_expropiada parcela_expropiada_objeto_expropiacion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela_expropiada
    ADD CONSTRAINT parcela_expropiada_objeto_expropiacion_fk FOREIGN KEY (objeto) REFERENCES public.objeto_expropiacion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: parcela parcela_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parcela
    ADD CONSTRAINT parcela_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: plano_mensura_intervencion plano_mensura_intervencion_idintervencion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_intervencion
    ADD CONSTRAINT plano_mensura_intervencion_idintervencion_fkey FOREIGN KEY (idintervencion) REFERENCES public.intervencion(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: plano_mensura_intervencion plano_mensura_intervencion_idplano_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_intervencion
    ADD CONSTRAINT plano_mensura_intervencion_idplano_fkey FOREIGN KEY (idplano) REFERENCES public.plano_mensura(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: plano_mensura_tierra plano_mensura_tierra_idplano_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_tierra
    ADD CONSTRAINT plano_mensura_tierra_idplano_fkey FOREIGN KEY (idplano) REFERENCES public.plano_mensura(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: plano_mensura_tierra plano_mensura_tierra_idtierra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plano_mensura_tierra
    ADD CONSTRAINT plano_mensura_tierra_idtierra_fkey FOREIGN KEY (idtierra) REFERENCES public.tierra(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: tierra tierra_destino_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra
    ADD CONSTRAINT tierra_destino_fkey FOREIGN KEY (destino) REFERENCES public.tierra_destino(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: tierra tierra_localidad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra
    ADD CONSTRAINT tierra_localidad_fkey FOREIGN KEY (localidad) REFERENCES public.localidad(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: tierra tierra_tipo_doc_probatoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tierra
    ADD CONSTRAINT tierra_tipo_doc_probatoria_fkey FOREIGN KEY (tipo_doc_probatoria) REFERENCES public.tipo_doc_probatoria(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: uf uf_parcela_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uf
    ADD CONSTRAINT uf_parcela_fk FOREIGN KEY (id_parcela) REFERENCES public.parcela(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: uf uf_res_costos_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uf
    ADD CONSTRAINT uf_res_costos_fkey FOREIGN KEY (res_costos) REFERENCES public.resolucion_costos(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: uf uf_tipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.uf
    ADD CONSTRAINT uf_tipo_fkey FOREIGN KEY (tipo) REFERENCES public.tipo_uf(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: vivienda_punto vivienda_punto_intervencion_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vivienda_punto
    ADD CONSTRAINT vivienda_punto_intervencion_fk FOREIGN KEY (id_intervencion) REFERENCES public.intervencion(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: vivienda_punto vivienda_punto_resolucion_costos_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vivienda_punto
    ADD CONSTRAINT vivienda_punto_resolucion_costos_fk FOREIGN KEY (res_costos) REFERENCES public.resolucion_costos(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: role role_group_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.role
    ADD CONSTRAINT role_group_fkey FOREIGN KEY ("group") REFERENCES visualizador.rolegroup(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: rolemapping rolemapping_created_by_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping
    ADD CONSTRAINT rolemapping_created_by_fkey FOREIGN KEY (created_by) REFERENCES visualizador."user"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: rolemapping rolemapping_role_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping
    ADD CONSTRAINT rolemapping_role_fkey FOREIGN KEY (role) REFERENCES visualizador.role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: rolemapping rolemapping_user_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador.rolemapping
    ADD CONSTRAINT rolemapping_user_fkey FOREIGN KEY ("user") REFERENCES visualizador."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user user_area_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador."user"
    ADD CONSTRAINT user_area_fkey FOREIGN KEY (area) REFERENCES visualizador.area(id);


--
-- Name: user user_created_by_fkey; Type: FK CONSTRAINT; Schema: visualizador; Owner: -
--

ALTER TABLE ONLY visualizador."user"
    ADD CONSTRAINT user_created_by_fkey FOREIGN KEY (created_by) REFERENCES visualizador."user"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--


