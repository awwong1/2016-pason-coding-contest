import json
import unittest
from algorithm import Algorithm, Map, Obstacle, Tank, Player


class TestAlgorithm(unittest.TestCase):
    raw_string = (
        '{"timeRemaining": 127.23818278312683, '
        '"map": {"terrain": ['
        '{"boundingBox": {"corner": [120, 200], "size": [60, 360]}, "type": "SOLID"}, '
        '{"boundingBox": {"corner": [360, 280], "size": [60, 400]}, "type": "SOLID"}, '
        '{"boundingBox": {"corner": [360, 0], "size": [60, 120]}, "type": "SOLID"}, '
        '{"boundingBox": {"corner": [600, 0], "size": [60, 200]}, "type": "SOLID"}], '
        '"size": [800, 450]}, '
        '"match_id": "9e1e91e5-dc19-4f4b-a8f9-7dbf057b2be1", '
        '"players": ['
        '{"score": 0, "name": "testclient", '
        '"tanks": ['
        '{"alive": true, "projectiles": [], "tracks": 5.082649623186166, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "19ba2d12-f51f-4c74-affc-6eebdc447921", "turret": 2.877371653791148, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [774, 201], "type": "TankFast"}, '
        '{"alive": true, "projectiles": [], "tracks": 0.2789576280213871, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "8a54890e-4cfb-45a7-8c51-2b8f2fa503f4", "turret": 1.4528153647376105, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [563, 123], "type": "TankFast"}, '
        '{"alive": true, "projectiles": [], "tracks": 2.6154451048166374, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "f147cffe-7f70-424a-972e-5ba6587a5f8e", "turret": 2.744946885711423, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [73, 200], "type": "TankFast"}, '
        '{"alive": true, "projectiles": [], "tracks": 5.875311234827194, "hitRadius": 2.0, '
        '"speed": 5.0, "id": "7c3ed564-7dd4-408f-8800-d6b38a36be6d", "turret": 4.182292475910125, '
        '"health": 200.0, "collisionRadius": 2.0, "position": [27, 90], "type": "TankSlow"}]}, '
        '{"score": 0, "name": "testclient2", '
        '"tanks": [{"alive": true, "projectiles": [], "tracks": 5.107883490393385, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "60b86760-42d4-4f77-8211-735f4bac919c", "turret": 0.8267392827046591, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [434, 297], "type": "TankFast"}, '
        '{"alive": true, "projectiles": [], "tracks": 1.9092326651351095, "hitRadius": 2.0, '
        '"speed": 5.0, "id": "b96e5c17-fd0c-43dc-b13f-65e7a4deff0c", "turret": 1.5968619660639252, '
        '"health": 200.0, "collisionRadius": 2.0, "position": [479, 193], "type": "TankSlow"}, '
        '{"alive": true, "projectiles": [], "tracks": 0.7852441041942855, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "9658f436-f826-4bc9-876a-6737564160f6", "turret": 4.874631386354732, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [758, 35], "type": "TankFast"}, '
        '{"alive": true, "projectiles": [], "tracks": 3.944628452197919, "hitRadius": 2.0, '
        '"speed": 10.0, "id": "fd9fb60c-18ee-43a6-a00d-93b30c7b812a", "turret": 1.277435287550733, '
        '"health": 100.0, "collisionRadius": 2.0, "position": [674, 386], "type": "TankFast"}]}], '
        '"timestamp": 1449703170887.637, "comm_type": "GAMESTATE"}'
    )
    json_game_state = json.loads(raw_string)

    def test_parse_game_state(self):
        self.maxDiff = None
        algo = Algorithm('testclient')
        algo.parse_game_state(self.json_game_state)
        self.assertEqual(algo.time_remaining, 127.23818278312683)
        obstacles = [
            Obstacle('SOLID', [120, 200], [60, 360]),
            Obstacle('SOLID', [360, 280], [60, 400]),
            Obstacle('SOLID', [360, 0], [60, 120]),
            Obstacle('SOLID', [600, 0], [60, 200])
        ]
        self.assertEqual(algo.map, Map((800, 450), obstacles))

        test_client_tanks = [
            Tank('19ba2d12-f51f-4c74-affc-6eebdc447921', 100.0, 2.0, 2.0, 'TankFast', [774, 201], 5.082649623186166,
                 2.877371653791148, 10.0, []),
            Tank('8a54890e-4cfb-45a7-8c51-2b8f2fa503f4', 100.0, 2.0, 2.0, 'TankFast', [563, 123], 0.2789576280213871,
                 1.4528153647376105, 10.0, []),
            Tank('f147cffe-7f70-424a-972e-5ba6587a5f8e', 100.0, 2.0, 2.0, 'TankFast', [73, 200], 2.61544510482,
                 2.744946885711423, 10.0, []),
            Tank('7c3ed564-7dd4-408f-8800-d6b38a36be6d', 200.0, 2.0, 2.0, 'TankSlow', [27, 90], 5.875311234827194,
                 4.182292475910125, 5.0, [])
        ]
        test_client_2_tanks = [
            Tank('60b86760-42d4-4f77-8211-735f4bac919c', 100.0, 2.0, 2.0, 'TankFast', [434, 297], 5.107883490393385,
                 0.8267392827046591, 10.0, []),
            Tank('b96e5c17-fd0c-43dc-b13f-65e7a4deff0c', 200.0, 2.0, 2.0, 'TankSlow', [479, 193], 1.9092326651351095,
                 1.5968619660639252, 5.0, []),
            Tank('9658f436-f826-4bc9-876a-6737564160f6', 100.0, 2.0, 2.0, 'TankFast', [758, 35], 0.7852441041942855,
                 4.874631386354732, 10.0, []),
            Tank('fd9fb60c-18ee-43a6-a00d-93b30c7b812a', 100.0, 2.0, 2.0, 'TankFast', [674, 386], 3.944628452197919,
                 1.277435287550733, 10.0, [])
        ]
        players = [
            Player('testclient', 0, test_client_tanks),
            Player('testclient2', 0, test_client_2_tanks)
        ]

        self.assertEquals(str(algo.players), str(players))
        self.assertEquals(algo.players, players)


if __name__ == '__main__':
    unittest.main()
