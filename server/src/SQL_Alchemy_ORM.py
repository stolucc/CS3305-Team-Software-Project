# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy import Column, Integer, String, Sequence, create_engine,\
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


connection, meta, session = connect("postgres", "password", "test")
session = session()
Base = declarative_base()


class TestTable(Base):
    __tablename__ = 'test_table'

    id = Column(Integer, Sequence('test_table_id_seq'), primary_key=True)
    first_name = Column(String(100))
    second_name = Column(String(100))

    def __repr__(self):
        return "<test_table(id='%s', name='%s', fullname='%s')>" % (
            self.id, self.first_name, self.second_name)


Base.metadata.create_all(connection)

# noinspection PyArgumentList
test_user = TestTable(first_name="Daragh", second_name="O'Sullivan")
session.add(test_user)
print(test_user.id)
print(test_user.first_name)

our_user = session.query(TestTable).filter_by(first_name='Daragh').first()
print(our_user)

# noinspection PyArgumentList
session.add_all([
    TestTable(first_name="Tom", second_name="Murphy"),
    TestTable(first_name="Billy", second_name="Connor"),
    TestTable(first_name="Scott", second_name="O'Brien")])

session.commit()

print(test_user.id)

for instance in session.query(TestTable).order_by(TestTable.id):
    print(instance.first_name, instance.second_name)
