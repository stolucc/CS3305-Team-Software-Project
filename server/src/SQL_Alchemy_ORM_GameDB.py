from sqlalchemy import Column, Integer, Boolean, ForeignKey, \
    Sequence, create_engine, MetaData, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


def connect(user, password, db, host="localhost", port=5432):
    """Returns a connection and a metadata object"""
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    c = create_engine(url, client_encoding="utf8")
    s = sessionmaker(bind=c)
    m = MetaData(bind=c, reflect=True)

    return c, m, s


connection, meta, session = connect("postgres", "password", "gamedb")
session = session()
Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, Sequence('games_game_id_seq'), primary_key=True)
    seed = Column(Integer, CheckConstraint('seed>=0'), nullable=False)
    active = Column(Boolean, nullable=False)

    users = relationship("User", back_populates="game", passive_deletes="all")

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

    def __repr__(self):
        return "<user(game_id='%s', user_id='%s', active='%s', " \
               "gold='%i', production='%i', food='%i', science='%i')>" % (
                self.game_id, self.user_id, self.active,
                self.gold, self.production, self.food, self.science)


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

    def __repr__(self):
        return "<unit(user_id='%s', unit_id='%s', " \
               "type='%s', health='%s', x='%s', y='%s', z='%s')>" % (
                self.user_id, self.unit_id,
                self.type, self.health, self.x, self.y, self.z)


class Technology(Base):
    __tablename__ = 'technologies'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    technology_id = Column(Integer, primary_key=True)

    user = relationship("User", back_populates="technologies")

    def __repr__(self):
        return"<technology(user_id='%s', technology_id='%s')>" % (
                self.user_id, self.technology_id)


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

    def __repr__(self):
        return "<building(user_id='%s', building_id='%s', " \
               "type='%s', x='%s', y='%s', z='%s')>" % (
                self.user_id, self.building_id,
                self.type, self.x, self.y, self.z)


Base.metadata.create_all(connection)

test_game = Game(seed=123456789, active=True)
session.add(test_game)
session.commit()

test_user = User(game_id=test_game.game_id, active=True,
                 gold=0, production=0, food=0, science=0)
session.add(test_user)
session.commit()

test_unit = Unit(user_id=test_user.user_id, type=0, health=100, x=5, y=4, z=2)
session.add(test_unit)
session.commit()

test_technology = Technology(user_id=test_user.user_id, technology_id=10)
session.add(test_technology)
session.commit()

test_building = Building(user_id=test_user.user_id, type=0, x=3, y=1, z=0)
session.add(test_building)
session.commit()

session.delete(test_game)
session.commit()

# for user in test_game.users:
#     print(user)
#
# for technology in test_user.technologies:
#     print(technology)
#
# for building in test_user.buildings:
#     print(building)
#
# for unit in test_user.units:
#     print(unit)
