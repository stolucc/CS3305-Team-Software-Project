-- Table: public.games

-- DROP TABLE public.games;

CREATE SEQUENCE games_game_id_seq;
CREATE TABLE public.games
(
  game_id INTEGER NOT NULL DEFAULT nextval('games_game_id_seq'),
  seed INTEGER NOT NULL,
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
  gold INTEGER NOT NULL,
  production INTEGER NOT NULL,
  food INTEGER NOT NULL,
  science INTEGER NOT NULL,
  CONSTRAINT user_id PRIMARY KEY (user_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.users OWNER TO postgres;
ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;

-- Table: public.technology

-- DROP TABLE public.technology;

CREATE TABLE public.technology
(
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  technology_id INTEGER NOT NULL,
  CONSTRAINT user_technology_id PRIMARY KEY (user_id, technology_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.technology OWNER TO postgres;

-- Table: public.buildings

-- DROP TABLE public.buildings;

CREATE SEQUENCE buildings_building_id_seq;
CREATE TABLE public.buildings
(
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  building_id INTEGER NOT NULL DEFAULT nextval('buildings_building_id_seq'),
  type VARCHAR(100) NOT NULL,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  CONSTRAINT user_building_id PRIMARY KEY (user_id, building_id)
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
  type VARCHAR(100) NOT NULL,
  health INTEGER NOT NULL,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  CONSTRAINT user_unit_id PRIMARY KEY (user_id, unit_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.units OWNER TO postgres;
ALTER SEQUENCE units_unit_id_seq OWNED BY units.unit_id;