# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy import Column, Integer, Boolean, String, Sequence, create_engine,\
    MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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


Base.metadata.create_all(connection)

# noinspection PyArgumentList
test_game = Game(seed=123456789, active=True)
session.add(test_game)
print(test_game.game_id)
print(test_game.seed)

our_game = session.query(Game).filter_by(seed=123456789).first()
print(our_game)

# noinspection PyArgumentList
session.add_all([
    Game(seed=987654321, active=False),
    Game(seed=135797531, active=False),
    Game(seed=246808642, active=False)])

session.commit()

print(test_game.game_id)

for instance in session.query(Game).order_by(Game.game_id):
    print(instance.seed, instance.active)
