"""Server Database API."""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, \
    Sequence, create_engine, MetaData, CheckConstraint, String, TIMESTAMP, \
    BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


class Connection:
    """Class to create a connection to the database."""

    def __init__(self, user, password, db, host="localhost", port=5432):
        """
        Create a Connection.

        :param user: username for the database
        :param password: password for the database
        :param db: database to connect to
        :param host: host that the database is running on. Default: localhost
        :param port: port that the database is listening on. Default: 5432
        """
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        self.connection = create_engine(url, client_encoding="utf8")
        self.session = sessionmaker(bind=self.connection)
        self.meta = MetaData(bind=self.connection)

    def get_connection(self):
        """Return a connection object."""
        return self.connection

    def get_session(self):
        """Return a session maker object."""
        return self.session

    def get_meta(self):
        """Return a meta object."""
        return self.meta


Base = declarative_base()


class Game(Base):
    """SQL Alchemy class to model the games database table."""

    __tablename__ = 'games'

    game_id = Column(Integer, Sequence('games_game_id_seq'), primary_key=True)
    seed = Column(Integer, CheckConstraint('seed>=0'), nullable=False)
    active = Column(Boolean, nullable=False)

    users = relationship("User", back_populates="game", passive_deletes="all")

    @staticmethod
    def insert_game(session, seed, active):
        """
        Create a game and add it to the database.

        :param session: sessionmaker object
        :param seed: map seed for the game. Must be >= 0.
        :param active: specifies if the game is active or not
        """
        game = Game(seed=seed, active=active)
        session = session()
        session.add(game)
        session.commit()
        game_id = game.game_id
        session.close()
        return game_id

    @staticmethod
    def select_game(session, game_id):
        """
        Select a game that is in the database.

        :param session: sessionmaker object
        :param game_id: game_id of the game to be selected
        """
        session = session()
        game = session.query(Game).filter(Game.game_id == game_id).first()
        game_dict = game.__dict__
        del game_dict['_sa_instance_state']
        session.close()
        return game_dict

    @staticmethod
    def update_game(session, game_id, **kwargs):
        """
        Update a game that is in the database.
        Updatable columns: seed, active

        :param session: sessionmaker object
        :param game_id: game_id of the game to be updated
        """
        session = session()
        game = session.query(Game).filter(Game.game_id == game_id).first()
        for name, value in kwargs.items():
            setattr(game, name, value)
        session.commit()
        session.close()

    @staticmethod
    def delete_game(session, game_id):
        """
        Delete a game from the database.

        :param session: sessionmaker object
        :param game_id: game_id of the game to be deleted
        """
        session = session()
        game = session.query(Game).filter(Game.game_id == game_id).first()
        session.delete(game)
        session.commit()
        session.close()

    def __repr__(self):
        """Return a String representation for a Game object."""
        return "<game(game_id='%s', seed='%d', active='%s')>" % (
            self.game_id, self.seed, self.active)


class User(Base):
    """SQL Alchemy class to model the users database table."""

    __tablename__ = 'users'

    game_id = Column(Integer, ForeignKey('games.game_id'))
    user_id = Column(Integer, Sequence('users_user_id_seq'), primary_key=True)
    active = Column(Boolean, nullable=False)
    gold = Column(Integer, CheckConstraint('gold>=0'), nullable=False)
    production = Column(Integer, CheckConstraint('production>=0'),
                        nullable=False)
    food = Column(Integer, CheckConstraint('food>=0'), nullable=False)
    science = Column(Integer, CheckConstraint('science>=0'), nullable=False)

    game = relationship("Game", back_populates="users")
    units = relationship("Unit", back_populates="user", passive_deletes="all")
    technologies = relationship("Technology", back_populates="user",
                                passive_deletes="all")
    buildings = relationship("Building", back_populates="user",
                             passive_deletes="all")

    @staticmethod
    def insert_user(session, game_id, active, gold, production, food, science):
        """
        Create a user and add it to the database.

        :param session: sessionmaker object
        :param game_id: game_id of the game that the user will be playing in
        :param active: specifies if the user is active or not
        :param gold: specifies the amount of gold the user has. Must be >= 0.
        :param production: specifies the amount of production the user has.
        Must be >= 0.
        :param food: specifies the amount of food the user has. Must be >= 0.
        :param science: specifies the amount of science the user has.
        Must be >= 0.
        """
        user = User(game_id=game_id, active=active, gold=gold,
                    production=production, food=food, science=science)
        session = session()
        session.add(user)
        session.commit()
        user_id = user.user_id
        session.close()
        return user_id

    @staticmethod
    def select_user(session, user_id):
        """
        Select a user that is in the database.

        :param session: sessionmaker object
        :param user_id: user_id of the user to be selected
        """
        session = session()
        user = session.query(User).filter(User.user_id == user_id).first()
        user_dict = user.__dict__
        del user_dict['_sa_instance_state']
        session.close()
        return user_dict

    @staticmethod
    def update_user(session, user_id, **kwargs):
        """
        Update a user that is in the database.
        Updatable columns: game_id, active, gold, production, food, science

        :param session: sessionmaker object
        :param user_id: user_id of the user to be updated
        """
        session = session()
        user = session.query(User).filter(User.user_id == user_id).first()
        for name, value in kwargs.items():
            setattr(user, name, value)
        session.commit()
        session.close()

    @staticmethod
    def delete_user(session, user_id):
        """
        Delete a user from the database.

        :param session: sessionmaker object
        :param user_id: user_id of the user to be deleted
        """
        session = session()
        user = session.query(User).filter(User.user_id == user_id).first()
        session.delete(user)
        session.commit()
        session.close()

    def __repr__(self):
        """Return a String representation for a User object."""
        return "<user(game_id='%s', user_id='%s', active='%s', " \
               "gold='%i', production='%i', food='%i', science='%i')>" % (
                   self.game_id, self.user_id, self.active,
                   self.gold, self.production, self.food, self.science)


class Technology(Base):
    """SQL Alchemy class to model the technologies database table."""

    __tablename__ = 'technologies'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    technology_id = Column(Integer, primary_key=True)

    user = relationship("User", back_populates="technologies")

    @staticmethod
    def insert_technology(session, user_id, technology_id):
        """
        Create a technology and add it to the database.

        :param session: sessionmaker object
        :param user_id: user_id of the user that has researched the technology
        :param technology_id: id of the technology researched. Must be >= 0.
        """
        technology = Technology(user_id=user_id, technology_id=technology_id)
        session = session()
        session.add(technology)
        session.commit()
        session.close()

    @staticmethod
    def select_technology(session, user_id, technology_id):
        """
        Select a technology that is in the database.

        :param session: sessionmaker object
        :param user_id: user_id of the technology to be selected
        :param user_id: technology_id of the technology to be selected
        """
        session = session()
        technology = session.query(Technology).filter(
            Technology.user_id == user_id,
            Technology.technology_id == technology_id).first()
        technology_dict = technology.__dict__
        del technology_dict['_sa_instance_state']
        session.close()
        return technology_dict

    @staticmethod
    def update_technology(session, user_id, **kwargs):
        """
        Update a technology that is in the database.
        Updatable columns: technology_id

        :param session: sessionmaker object
        :param user_id: user_id of the technology to be updated
        """
        session = session()
        technology = session.query(Technology).filter(
            Technology.user_id == user_id).first()
        for name, value in kwargs.items():
            setattr(technology, name, value)
        session.commit()
        session.close()

    @staticmethod
    def delete_technology(session, user_id, technology_id):
        """
        Delete a technology from the database.

        :param session: sessionmaker object
        :param user_id: user_id of the technology to be deleted
        :param technology_id: technology_id of the technology to be deleted.
        Must be >= 0.
        """
        session = session()
        technology = session.query(Technology).filter(
            Technology.user_id == user_id,
            Technology.technology_id == technology_id).first()
        session.delete(technology)
        session.commit()
        session.close()

    def __repr__(self):
        """Return a String representation for a Technology object."""
        return"<technology(user_id='%s', technology_id='%s')>" % (
            self.user_id, self.technology_id)


class Unit(Base):
    """SQL Alchemy class to model the units database table."""

    __tablename__ = 'units'

    user_id = Column(Integer, ForeignKey('users.user_id'))
    unit_id = Column(Integer, Sequence('units_unit_id_seq'), primary_key=True)
    type = Column(Integer, CheckConstraint('type>=0'),  nullable=False)
    health = Column(Integer, CheckConstraint('health>=0'), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    user = relationship("User", back_populates="units")

    @staticmethod
    def insert_unit(session, user_id, type, health, x, y, z):
        """
        Create a unit and add it to the database.

        :param session: sessionmaker object
        :param user_id: user_id of the user that owns the unit
        :param type: specifies the type of unit. Must be >= 0.
        :param health: specifies the health of unit. Must be >= 0.
        :param x: specifies the location (x coordinate) of unit.
        x + y + z must equal 0.
        :param y: specifies the location (y coordinate) of unit.
        x + y + z must equal 0.
        :param z: specifies the location (z coordinate) of unit.
        x + y + z must equal 0.
        """
        unit = Unit(user_id=user_id, type=type, health=health, x=x, y=y,
                    z=z)
        session = session()
        session.add(unit)
        session.commit()
        unit_id = unit.unit_id
        session.close()
        return unit_id

    @staticmethod
    def select_unit(session, unit_id):
        """
        Select a unit that is in the database.

        :param session: sessionmaker object
        :param unit_id: unit_id of the unit to be selected
        """
        session = session()
        unit = session.query(Unit).filter(Unit.unit_id == unit_id).first()
        unit_dict = unit.__dict__
        del unit_dict['_sa_instance_state']
        session.close()
        return unit_dict

    @staticmethod
    def update_unit(session, unit_id, **kwargs):
        """
        Update a unit that is in the database.
        Updatable columns: type, health, x, y, z

        :param session: sessionmaker object
        :param unit_id: unit_id of the unit to be updated
        """
        session = session()
        unit = session.query(Unit).filter(
            Unit.unit_id == unit_id).first()
        for name, value in kwargs.items():
            setattr(unit, name, value)
        session.commit()
        session.close()

    @staticmethod
    def delete_unit(session, unit_id):
        """
        Delete a unit from the database.

        :param session: sessionmaker object
        :param unit_id: unit_id of the unit to be deleted
        """
        session = session()
        unit = session.query(Unit).filter(Unit.unit_id == unit_id).first()
        session.delete(unit)
        session.commit()
        session.close()

    def __repr__(self):
        """Return a String representation for a Unit object."""
        return "<unit(user_id='%s', unit_id='%s', " \
               "type='%s', health='%s', x='%s', y='%s', z='%s')>" % (
                   self.user_id, self.unit_id,
                   self.type, self.health, self.x, self.y, self.z)


class Building(Base):
    """SQL Alchemy class to model the buildings database table."""

    __tablename__ = 'buildings'

    user_id = Column(Integer, ForeignKey('users.user_id'))
    building_id = Column(Integer, Sequence('buildings_building_id_seq'),
                         primary_key=True)
    type = Column(Integer, CheckConstraint('type>=0'), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    user = relationship("User", back_populates="buildings")

    @staticmethod
    def insert_building(session, user_id, type, x, y, z):
        """
        Create a building and add it to the database.

        :param session: sessionmaker object
        :param user_id: user_id of the user that owns the building
        :param type: specifies the type of building. Must be >= 0.
        :param x: specifies the location (x coordinate) of building.
        x + y + z must equal 0.
        :param y: specifies the location (y coordinate) of building.
        x + y + z must equal 0.
        :param z: specifies the location (z coordinate) of building.
        x + y + z must equal 0.
        """
        building = Building(user_id=user_id, type=type, x=x, y=y, z=z)
        session = session()
        session.add(building)
        session.commit()
        building_id = building.building_id
        session.close()
        return building_id

    @staticmethod
    def select_building(session, building_id):
        """
        Select a building_id that is in the database.

        :param session: sessionmaker object
        :param building_id: building_id of the building to be selected
        """
        session = session()
        building_id = session.query(Building).filter(
            Building.building_id == building_id).first()
        building_id_dict = building_id.__dict__
        del building_id_dict['_sa_instance_state']
        session.close()
        return building_id_dict

    @staticmethod
    def update_building(session, building_id, **kwargs):
        """
        Update a building that is in the database.
        Updatable columns: type, x, y, z

        :param session: sessionmaker object
        :param building_id: building_id of the building to be updated
        """
        session = session()
        building = session.query(Building).filter(
            Building.building_id == building_id).first()
        for name, value in kwargs.items():
            setattr(building, name, value)
        session.commit()
        session.close()

    @staticmethod
    def delete_building(session, building_id):
        """
        Delete a building from the database.

        :param session: sessionmaker object
        :param building_id: building_id of the unit to be deleted
        """
        session = session()
        building = session.query(Building).filter(
            Building.building_id == building_id).first()
        session.delete(building)
        session.commit()
        session.close()

    def __repr__(self):
        """Return a String representation for a Building object."""
        return "<building(user_id='%s', building_id='%s', " \
               "type='%s', x='%s', y='%s', z='%s')>" % (
                   self.user_id, self.building_id,
                   self.type, self.x, self.y, self.z)


class Log(Base):
    """SQL Alchemy class to model the logs database table."""

    __tablename__ = 'logs'

    log_id = Column(Integer, Sequence('logs_log_id_seq'), primary_key=True)
    log_level = Column(Integer, CheckConstraint('log_level>=0'),
                       nullable=False)
    log_level_name = Column(String(256), nullable=False)
    file_name = Column(String(256), nullable=False)
    line_number = Column(Integer, CheckConstraint('line_number>=0'),
                         nullable=False)
    function_name = Column(String(256), nullable=False)
    log = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, CheckConstraint('created_at>=0'),
                        nullable=False)
    created_by = Column(String(256), nullable=False)
    process_id = Column(BIGINT, CheckConstraint('process_id>=0'),
                        nullable=False)
    process_name = Column(String(256), nullable=False)
    thread_id = Column(BIGINT, CheckConstraint('thread_id>=0'),
                       nullable=False)
    thread_name = Column(String(256), nullable=False)

    @staticmethod
    def insert_log(session, log_level, log_level_name, file_name, line_number,
                   function_name, log, created_at, created_by, process_id,
                   process_name, thread_id, thread_name):
        """
        Create a log and add it to the database.

        :param session: sessionmaker object
        :param log_level: log_level of the log. Must be >= 0.
        :param log_level_name: log_level_name of the log
        (limit is 256 characters)
        :param file_name: filename of the file where the logging call was made
        (limit is 256 characters)
        :param line_number: line number in the file where the logging call was
        made. Must be >= 0.
        :param function_name: name of function where the logging call was
        made. (limit is 256 characters)
        :param log: log message of the log (limit is 2048 characters)
        :param created_at: timestamp of when the log was created
        :param created_by: what created the log (limit is 256 characters)
        :param process_id: id of the process that created the log.
        Must be >= 0.
        :param process_name: name of the process that created the log
        (limit is 256 characters)
        :param thread_id: id of the thread that created the log.
        Must be >= 0.
        :param thread_name: name of the thread that created the log
        (limit is 256 characters)
        """
        log = Log(log_level=log_level, log_level_name=log_level_name,
                  file_name=file_name, line_number=line_number,
                  function_name=function_name, log=log, created_at=created_at,
                  created_by=created_by, process_id=process_id,
                  process_name=process_name, thread_id=thread_id,
                  thread_name=thread_name)
        session = session()
        session.add(log)
        session.commit()
        log_id = log.log_id
        session.close()
        return log_id

    def __repr__(self):
        """Return a String representation for a Log object."""
        return "<log(log_id='%s', log_level='%s', log_level_name='%s', " \
               "file_name='%s', line_number='%s', function_name='%s' " \
               "log='%s', created_at='%s', created_by='%s' process_id='%s', " \
               "process_name='%s', thread_id='%s', thread_name='%s')>" % (
                   self.log_id, self.log_level, self.log_level_name,
                   self.file_name, self.line_number, self.function_name,
                   self.log, self.created_at, self.created_by, self.process_id,
                   self.process_name, self.thread_id, self.thread_name)
