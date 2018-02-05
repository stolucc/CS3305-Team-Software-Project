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
        game_id = Game.insert(session, 1, True)
        assert type(game_id) is int, "Can't insert game to database"

    def test_select_game(self):
        """Select a game in the database"""
        game_id = Game.insert(session, 1, True)
        game_dict = Game.select(session, game_id)
        assert game_dict == {'game_id': game_id, 'active': True, 'seed': 1}, \
            "Can't select game from database"

    def test_update_game(self):
        """Update a game in the database"""
        game_id = Game.insert(session, 1, True)
        Game.update(session, game_id, seed=2, active=False)
        game_dict = Game.select(session, game_id)
        assert game_dict == {'game_id': game_id, 'active': False, 'seed': 2}, \
            "Can't update game in database"

    def test_insert_user(self):
        """Insert a user to the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        assert type(user_id) is int, "Can't insert user to database"

    def test_select_user(self):
        """Select a user in the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        user_dict = User.select(session, user_id)
        assert user_dict == {'game_id': game_id, 'user_id': user_id,
                             'active': True, 'gold': 0, 'production': 0,
                             'food': 0, 'science': 0}, \
            "Can't select user from database"

    def test_update_user(self):
        """Update a user in the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        User.update(session, user_id, game_id=game_id, active=False,
                    gold=10, production=20, food=30, science=40)
        user_dict = User.select(session, user_id)
        assert user_dict == {'game_id': game_id, 'user_id': user_id,
                             'active': False, 'gold': 10, 'production': 20,
                             'food': 30, 'science': 40}, \
            "Can't update user in database"

    def test_insert_technology(self):
        """Insert a technology to the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        Technology.insert(session, user_id, 1)

    def test_select_technology(self):
        """Select a technology in the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        Technology.insert(session, user_id, 1)
        technology_dict = Technology.select(session, user_id, 1)
        assert technology_dict == {'user_id': user_id,
                                   'technology_id': 1}, \
            "Can't select technology from database"

    def test_update_technology(self):
        """Update a technology in the database"""
        game_id = Game.insert(session, 1, True)
        user_id1 = User.insert(session, game_id, True, 0, 0, 0, 0)
        user_id2 = User.insert(session, game_id, True, 0, 0, 0, 0)
        Technology.insert(session, user_id1, 1)
        Technology.update(session, user_id1, 1,
                          user_id=user_id2, technology_id=2)
        technology_dict = Technology.select(session, user_id2, 2)
        assert technology_dict == {'user_id': user_id2,
                                   'technology_id': 2}, \
            "Can't update technology in database"

    def test_insert_unit(self):
        """Insert a unit to the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        unit_id = Unit.insert(session, user_id, 0, 100, 0, 0, 0)
        assert type(unit_id) is int, "Can't insert game to database"

    def test_select_unit(self):
        """Select a unit in the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        unit_id = Unit.insert(session, user_id, 0, 100, 0, 0, 0)
        unit_dict = Unit.select(session, unit_id)
        assert unit_dict == {'user_id': user_id, 'unit_id': unit_id,
                             'type': 0, 'health': 100, 'x': 0, 'y': 0,
                             'z': 0}, \
            "Can't select unit from database"

    def test_update_unit(self):
        """Update a unit in the database"""
        game_id = Game.insert(session, 1, True)
        user_id1 = User.insert(session, game_id, True, 0, 0, 0, 0)
        user_id2 = User.insert(session, game_id, True, 0, 0, 0, 0)
        unit_id = Unit.insert(session, user_id1, 0, 100, 0, 0, 0)

        Unit.update(session, unit_id, user_id=user_id2, type=1,
                    health=90, x=3, y=-2, z=-1)
        unit_dict = Unit.select(session, unit_id)
        assert unit_dict == {'user_id': user_id2, 'unit_id': unit_id,
                             'type': 1, 'health': 90, 'x': 3, 'y': -2,
                             'z': -1}, \
            "Can't update unit in database"

    def test_insert_building(self):
        """Insert a building to the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        building_id = Building.insert(session, user_id, 0, 0, 0, 0)
        assert type(building_id) is int, "Can't insert game to database"

        Game.delete(session, game_id)

    def test_select_building(self):
        """Select a building in the database"""
        game_id = Game.insert(session, 1, True)
        user_id = User.insert(session, game_id, True, 0, 0, 0, 0)
        building_id = Building.insert(session, user_id, 0, 0, 0, 0)
        building_dict = Building.select(session, building_id)
        assert building_dict == {'user_id': user_id,
                                 'building_id': building_id,
                                 'type': 0, 'x': 0, 'y': 0, 'z': 0}, \
            "Can't select building from database"

    def test_update_building(self):
        """Update a unit in the database"""
        game_id = Game.insert(session, 1, True)
        user_id1 = User.insert(session, game_id, True, 0, 0, 0, 0)
        user_id2 = User.insert(session, game_id, True, 0, 0, 0, 0)
        building_id = Building.insert(session, user_id1, 0, 0, 0, 0)

        Building.update(session, building_id, user_id=user_id2,
                        type=1, x=3, y=-2, z=-1)
        building_dict = Building.select(session, building_id)
        assert building_dict == {'user_id': user_id2,
                             'building_id': building_id,
                             'type': 1, 'x': 3, 'y': -2, 'z': -1}, \
            "Can't update building in database"


if __name__ == "__main__":
    unittest.main()
