-- Table: public.games

-- DROP TABLE public.games;

CREATE SEQUENCE games_game_id_seq;
CREATE TABLE public.games
(
  game_id INTEGER NOT NULL DEFAULT nextval('games_game_id_seq'),
  seed INTEGER NOT NULL CHECK (seed >= 0),
  active BOOLEAN NOT NULL,
  CONSTRAINT game_id PRIMARY KEY (game_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.games OWNER TO postgres;
ALTER SEQUENCE games_game_id_seq OWNED BY games.game_id;

-- Table: public.users

-- DROP TABLE public.users;

CREATE SEQUENCE users_user_id_seq;
CREATE TABLE public.users
(
  game_id INTEGER NOT NULL REFERENCES games(game_id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL DEFAULT nextval('users_user_id_seq'),
  active BOOLEAN NOT NULL,
  gold INTEGER NOT NULL CHECK (gold >= 0),
  production INTEGER NOT NULL CHECK (production >= 0),
  food INTEGER NOT NULL CHECK (food >= 0),
  science INTEGER NOT NULL CHECK (science >= 0),
  CONSTRAINT user_id PRIMARY KEY (user_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.users OWNER TO postgres;
ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;

-- Table: public.technologies

-- DROP TABLE public.technologies;

CREATE TABLE public.technologies
(
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  technology_id INTEGER NOT NULL,
  CONSTRAINT user_technology_id PRIMARY KEY (user_id, technology_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.technologies OWNER TO postgres;

-- Table: public.buildings

-- DROP TABLE public.buildings;

CREATE SEQUENCE buildings_building_id_seq;
CREATE TABLE public.buildings
(
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  building_id INTEGER NOT NULL DEFAULT nextval('buildings_building_id_seq'),
  type INTEGER NOT NULL CHECK (type >= 0),
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  CONSTRAINT building_id PRIMARY KEY (building_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.buildings OWNER TO postgres;
ALTER SEQUENCE buildings_building_id_seq OWNED BY buildings.building_id;

-- Table: public.units

-- DROP TABLE public.units;

CREATE SEQUENCE units_unit_id_seq;
CREATE TABLE public.units
(
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  unit_id INTEGER NOT NULL DEFAULT nextval('units_unit_id_seq'),
  type INTEGER NOT NULL CHECK (type >= 0),
  health INTEGER NOT NULL CHECK (health >= 0),
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  CONSTRAINT unit_id PRIMARY KEY (unit_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.units OWNER TO postgres;
ALTER SEQUENCE units_unit_id_seq OWNED BY units.unit_id;

-- Table: public.logs

-- DROP TABLE public.logs;

CREATE SEQUENCE logs_log_id_seq;
CREATE TABLE public.logs
(
  log_id INTEGER NOT NULL DEFAULT nextval('logs_log_id_seq'),
  log_level INTEGER NOT NULL,
  log_level_name VARCHAR(128) NOT NULL,
  log VARCHAR(2048) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  created_by VARCHAR(128) NOT NULL,
  CONSTRAINT log_id PRIMARY KEY (log_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.logs OWNER TO postgres;
ALTER SEQUENCE logs_log_id_seq OWNED BY logs.log_id;