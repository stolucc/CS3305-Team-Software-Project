from sqlalchemy import Column, Integer, Boolean, ForeignKey, \
    Sequence, create_engine, MetaData, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


class Connection:
    def __init__(self, user, password, db, host="localhost", port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        self.connection = create_engine(url, client_encoding="utf8")
        self.session = sessionmaker(bind=self.connection)
        self.meta = MetaData(bind=self.connection)

    def get_connection(self):
        return self.connection

    def get_session(self):
        return self.session

    def get_meta(self):
        return self.meta


Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, Sequence('games_game_id_seq'), primary_key=True)
    seed = Column(Integer, CheckConstraint('seed>=0'), nullable=False)
    active = Column(Boolean, nullable=False)

    users = relationship("User", back_populates="game", passive_deletes="all")

    @staticmethod
    def insert_game(session, seed, active):
        game = Game(seed=seed, active=active)
        session = session()
        session.add(game)
        session.commit()
        game_id = game.game_id
        session.close()
        return game_id

    @staticmethod
    def delete_game(session, game_id):
        session = session()
        game = session.query(Game).filter(Game.game_id == game_id).first()
        session.delete(game)
        session.commit()
        session.close()

    def __repr__(self):
        return "<game(game_id='%s', seed='%d', active='%s')>" % (
            self.game_id, self.seed, self.active)


class User(Base):
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
        user = User(game_id=game_id, active=active, gold=gold,
                    production=production, food=food, science=science)
        session = session()
        session.add(user)
        session.commit()
        user_id = user.user_id
        session.close()
        return user_id

    @staticmethod
    def delete_user(session, user_id):
        session = session()
        user = session.query(User).filter(User.user_id == user_id).first()
        session.delete(user)
        session.commit()
        session.close()

    def __repr__(self):
        return "<user(game_id='%s', user_id='%s', active='%s', " \
               "gold='%i', production='%i', food='%i', science='%i')>" % (
                   self.game_id, self.user_id, self.active,
                   self.gold, self.production, self.food, self.science)


class Technology(Base):
    __tablename__ = 'technologies'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    technology_id = Column(Integer, primary_key=True)

    user = relationship("User", back_populates="technologies")

    @staticmethod
    def insert_technology(session, user_id, technology_id):
        technology = Technology(user_id=user_id, technology_id=technology_id)
        session = session()
        session.add(technology)
        session.commit()
        session.close()

    @staticmethod
    def delete_technology(session, user_id, technology_id):
        session = session()
        technology = session.query(Technology).filter(
            Technology.user_id == user_id,
            Technology.technology_id == technology_id).first()
        session.delete(technology)
        session.commit()
        session.close()

    def __repr__(self):
        return"<technology(user_id='%s', technology_id='%s')>" % (
            self.user_id, self.technology_id)


class Unit(Base):
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
        unit = Unit(user_id=user_id, type=type, health=health, x=x, y=y,
                    z=z)
        session = session()
        session.add(unit)
        session.commit()
        unit_id = unit.unit_id
        session.close()
        return unit_id

    @staticmethod
    def delete_unit(session, unit_id):
        session = session()
        unit = session.query(Unit).filter(Unit.unit_id == unit_id).first()
        session.delete(unit)
        session.commit()
        session.close()

    def __repr__(self):
        return "<unit(user_id='%s', unit_id='%s', " \
               "type='%s', health='%s', x='%s', y='%s', z='%s')>" % (
                   self.user_id, self.unit_id,
                   self.type, self.health, self.x, self.y, self.z)


class Building(Base):
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
        building = Building(user_id=user_id, type=type, x=x, y=y, z=z)
        session = session()
        session.add(building)
        session.commit()
        building_id = building.building_id
        session.close()
        return building_id

    @staticmethod
    def delete_building(session, building_id):
        session = session()
        building = session.query(Building).filter(
            Building.building_id == building_id).first()
        session.delete(building)
        session.commit()
        session.close()

    def __repr__(self):
        return "<building(user_id='%s', building_id='%s', " \
               "type='%s', x='%s', y='%s', z='%s')>" % (
                   self.user_id, self.building_id,
                   self.type, self.x, self.y, self.z)
