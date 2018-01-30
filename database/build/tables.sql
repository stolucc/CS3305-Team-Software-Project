-- Table: public.Games

-- DROP TABLE public.Games;

CREATE SEQUENCE Games_game_id_seq;
CREATE TABLE public.Games
(
  game_id INTEGER NOT NULL DEFAULT nextval('Games_game_id_seq'),
  seed INTEGER NOT NULL,
  active BOOLEAN NOT NULL,
  CONSTRAINT game_id PRIMARY KEY (game_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.Games OWNER TO postgres;
ALTER SEQUENCE Games_game_id_seq OWNED BY Games.game_id;

-- Table: public.Users

-- DROP TABLE public.Users;

CREATE SEQUENCE Users_user_id_seq;
CREATE TABLE public.Users
(
  game_id INTEGER NOT NULL REFERENCES Games(game_id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL DEFAULT nextval('Users_user_id_seq'),
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
ALTER TABLE public.Users OWNER TO postgres;
ALTER SEQUENCE Users_user_id_seq OWNED BY Users.user_id;

-- Table: public.Technology

-- DROP TABLE public.Technology;

CREATE TABLE public.Technology
(
  user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
  technology_id INTEGER NOT NULL,
  CONSTRAINT user_technology_id PRIMARY KEY (user_id, technology_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.Technology OWNER TO postgres;

-- Table: public.Buildings

-- DROP TABLE public.Buildings;

CREATE SEQUENCE Buildings_building_id_seq;
CREATE TABLE public.Buildings
(
  user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
  building_id INTEGER NOT NULL DEFAULT nextval('Buildings_building_id_seq'),
  type VARCHAR(100) NOT NULL,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  CONSTRAINT user_building_id PRIMARY KEY (user_id, building_id)
)
WITH (
OIDS=FALSE
);
ALTER TABLE public.Buildings OWNER TO postgres;
ALTER SEQUENCE Buildings_building_id_seq OWNED BY Buildings.building_id;

-- Table: public.Units

-- DROP TABLE public.Units;

CREATE SEQUENCE Units_unit_id_seq;
CREATE TABLE public.Units
(
  user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
  unit_id INTEGER NOT NULL DEFAULT nextval('Units_unit_id_seq'),
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
ALTER TABLE public.Units OWNER TO postgres;
ALTER SEQUENCE Units_unit_id_seq OWNED BY Units.unit_id;