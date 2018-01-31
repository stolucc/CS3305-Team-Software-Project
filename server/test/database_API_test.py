import unittest
from database_API import Connection, Game, User, Technology, Unit, Building

connection = Connection("postgres", "password", "gamedb")
session = connection.get_session()


class SimpleDatabaseTest(unittest.TestCase):

    def tearDown(self):
        connection = Connection("postgres", "password",
                                "gamedb").get_connection()
        connection.execute("DELETE FROM public.games;")
        pass

    def test_insert_game(self):
        """Insert a game to the database"""
        game_id = Game.insert_game(session, 1, True)
        assert type(game_id) is int, "Can't insert game to database"

    def test_insert_user(self):
        """Insert a user to the database"""
        game_id = Game.insert_game(session, 1, True)
        user_id = User.insert_user(session, game_id, True, 0, 0, 0, 0)
        assert type(user_id) is int, "Can't insert user to database"

    def test_insert_technology(self):
        """Insert a technology to the database"""
        game_id = Game.insert_game(session, 1, True)
        user_id = User.insert_user(session, game_id, True, 0, 0, 0, 0)
        Technology.insert_technology(session, user_id, 1)

    def test_insert_unit(self):
        """Insert a unit to the database"""
        game_id = Game.insert_game(session, 1, True)
        user_id = User.insert_user(session, game_id, True, 0, 0, 0, 0)
        unit_id = Unit.insert_unit(session, user_id, 0, 100, 0, 0, 0)
        assert type(unit_id) is int, "Can't insert game to database"

    def test_insert_building(self):
        """Insert a building to the database"""
        game_id = Game.insert_game(session, 1, True)
        user_id = User.insert_user(session, game_id, True, 0, 0, 0, 0)
        building_id = Building.insert_building(session, user_id, 0, 0, 0, 0)
        assert type(building_id) is int, "Can't insert game to database"

        Game.delete_game(session, game_id)


if __name__ == "__main__":
    unittest.main() # run all tests
