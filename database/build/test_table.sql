-- Table: public.test_table

-- DROP TABLE public.test_table;

CREATE SEQUENCE test_table_id_seq;
CREATE TABLE public.test_table
(
  id INTEGER NOT NULL DEFAULT nextval('test_table_id_seq'),
  first_name VARCHAR(100) NOT NULL,
  second_name VARCHAR(100) NOT NULL,
  CONSTRAINT id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.test_table OWNER TO postgres;
ALTER SEQUENCE test_table_id_seq OWNED BY test_table.id;
