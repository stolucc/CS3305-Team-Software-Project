# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, Sequence, create_engine,\
    MetaData
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


connection, meta, session = connect("postgres", "snoopy", "gamedb")
session = session()
Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, Sequence('games_game_id_seq'), primary_key=True)
    seed = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<game(game_id='%s', seed='%d', active='%s')>" % (
            self.game_id, self.seed, self.active)

class User(Base):
    __tablename__ = 'users'

    game_id = Column(Integer, ForeignKey('games.game_id'))
    user_id = Column(Integer, Sequence('users_user_id_seq'), primary_key=True)
    active = Column(Boolean, nullable=False)
    gold = Column(Integer, nullable=False)
    production = Column(Integer, nullable=False)
    food = Column(Integer, nullable=False)
    science = Column(Integer, nullable=False)
    
    game = relationship(Game, primaryjoin=game_id == Game.game_id, cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        return "<users(game='%s', user_id='%s', active='%s', gold='%i', production='%i', food='%i', science='%i')>" % (
            User.game, self.user_id, self.active, self.gold, self.production, self.food, self.science)

class Unit(Base):
    __tablename__ = 'units'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    unit_id = Column(Integer, Sequence('units_unit_id_seq'), primary_key=True)
    type = Column(String(100), nullable=False)
    health = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    user = relationship(User, primaryjoin=user_id == User.user_id, cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        return "<units(user='%s', unit_id='%s', type='%s', health='%s', x='%s', y='%s', z='%s')>" % (
            User.user_id, self.unit_id, self.type, self.health, self.x, self.y, self.z)

class Technology(Base):
    __tablename__ = 'technology'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    technology_id = Column(Integer, primary_key=True)

    user = relationship(User, primaryjoin=user_id == User.user_id, cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        return"<technology(user='%s', technology_id='%s')>" % (
            User.user_id, self.technology_id)

class Building(Base):
    __tablename__ = 'buildings'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    building_id = Column(Integer, Sequence('units_unit_id_seq'), primary_key=True)
    type = Column(String(100), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    user = relationship(User, primaryjoin=user_id == User.user_id, cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        return "<units(user='%s', building_id='%s', type='%s', x='%s', y='%s', z='%s')>" % (
            User.user_id, self.building_id, self.type, self.x, self.y, self.z)

Base.metadata.create_all(connection)

# noinspection PyArgumentList
test_game = Game(seed=123456789, active=True)
session.add(test_game)
session.commit()
id = test_game.game_id
print(id)

test_user = User(game_id=id, active=True, gold=0, production=0, food=0, science=0)
session.add(test_user)
session.commit()

uid = test_user.user_id

test_unit = Unit(user_id=uid, type='archer', health=100, x=5, y=4, z=2)
session.add(test_unit)
session.commit()

test_technology = Technology(user_id=uid, technology_id=10)
session.add(test_technology)
session.commit()

test_building = Building(user_id=uid, type="barracks", x=3, y=1, z=0)
session.add(test_building)
session.commit()

session.delete(test_game)
session.commit()
