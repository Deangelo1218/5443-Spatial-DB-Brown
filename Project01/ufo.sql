-- Table: public.aliens

-- DROP TABLE IF EXISTS public.aliens;

CREATE TABLE IF NOT EXISTS public.aliens
(
    datetime text COLLATE pg_catalog."default",
    country character varying(50) COLLATE pg_catalog."default",
    city character varying(50) COLLATE pg_catalog."default",
    state character varying(3) COLLATE pg_catalog."default",
    shape character varying(50) COLLATE pg_catalog."default",
    summary text COLLATE pg_catalog."default",
    lat real,
    lng real,
    id integer NOT NULL DEFAULT nextval('aliens_id_seq'::regclass),
    location geometry(Point,4326),
    CONSTRAINT aliens_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.aliens
    OWNER to postgres;
-- Index: city

-- DROP INDEX IF EXISTS public.city;

CREATE INDEX IF NOT EXISTS city
    ON public.aliens USING btree
    (city COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE(state)
    TABLESPACE pg_default;