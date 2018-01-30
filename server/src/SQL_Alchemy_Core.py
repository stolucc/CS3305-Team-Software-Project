# http://docs.sqlalchemy.org/en/latest/core/tutorial.html
import sqlalchemy


def connect(user, password, db, host="localhost", port=5432):
    """Returns a connection and a metadata object"""
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    c = sqlalchemy.create_engine(url, client_encoding="utf8")
    m = sqlalchemy.MetaData(bind=c, reflect=True)

    return c, m


connection, meta = connect("postgres", "snoopy", "test")

# List all tables
for table in meta.tables:
    print(table)

# Get table object
test_table = meta.tables["test_table"]

# Insert one row
clause = test_table.insert().values(
    first_name="Daragh",
    second_name="O'Sullivan")

# Inspect SQL generated
print(str(clause))

result = connection.execute(clause)

# Get inserted row's primary key
print(result.inserted_primary_key)

names = [
    {"first_name": "John", "second_name": "Connor"},
    {"first_name": "Sarah", "second_name": "Burke"},
    {"first_name": "Billy", "second_name": "Murphy"}]

# Insert multiple
connection.execute(test_table.insert(), names)


# Get columns
for col in test_table.c:
    print(col)

# Select
for row in connection.execute(test_table.select()):
    print(row)

# Select with where clause
clause = test_table.select().where(test_table.c.first_name == "Daragh")
for row in connection.execute(clause):
    print(row)

# Execute SQL
s = sqlalchemy.sql.text(
    """SELECT first_name, second_name
       FROM test_table
       WHERE test_table.id = :id""")
result = connection.execute(s, id=1)
for row in result:
    print(row)

# Delete data from table
#connection.execute(test_table.delete())
