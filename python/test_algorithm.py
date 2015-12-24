import json
import unittest
from algorithm import Algorithm
from game_objects.map import Map
from game_objects.obstacle import Obstacle
from game_objects.player import Player
from game_objects.projectile import Projectile
from game_objects.tank import Tank


class TestAlgorithm(unittest.TestCase):
    def test_parse_game_state(self):
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
        algo = Algorithm('testclient', 'pseudo_client_token')
        algo.parse_game_state(json_game_state)
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

    def test_get_tank_distances(self):
        tank_1 = Tank('tank_1', 100.0, 2.0, 2.0, 'TankFast', [0, 0], 0.0, 0.0, 10.0, [])
        tank_2 = Tank('tank_2', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        tank_3 = Tank('tank_3', 100.0, 2.0, 2.0, 'TankFast', [200, 200], 0.0, 0.0, 10.0, [])
        tank_4 = Tank('tank_4', 100.0, 2.0, 2.0, 'TankFast', [300, 300], 0.0, 0.0, 10.0, [])
        test_target_tanks = [tank_1, tank_2, tank_3, tank_4]

        origin_tank = Tank('origin_tank', 100.0, 2.0, 2.0, 'TankFast', [-1, -1], 0.0, 0.0, 10.0, [])
        self.assertEquals(origin_tank.get_all_dist_tank(test_target_tanks),
                          [(1.4142135623730951, tank_1), (142.8355697996826, tank_2), (284.2569260369921, tank_3),
                           (425.67828227430164, tank_4)])

    def test_get_closest_tank(self):
        tank_1 = Tank('tank_1', 100.0, 2.0, 2.0, 'TankFast', [0, 0], 0.0, 0.0, 10.0, [])
        tank_2 = Tank('tank_2', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        tank_3 = Tank('tank_3', 100.0, 2.0, 2.0, 'TankFast', [200, 200], 0.0, 0.0, 10.0, [])
        tank_4 = Tank('tank_4', 100.0, 2.0, 2.0, 'TankFast', [300, 300], 0.0, 0.0, 10.0, [])
        test_target_tanks = [tank_1, tank_2, tank_3, tank_4]

        origin_tank = Tank('origin_tank', 100.0, 2.0, 2.0, 'TankFast', [-1, -1], 0.0, 0.0, 10.0, [])
        closet_tank = origin_tank.get_closest_dist_tank(test_target_tanks)
        self.assertEquals(closet_tank, (1.4142135623730951, tank_1))

        origin_tank = Tank('origin_tank', 100.0, 2.0, 2.0, 'TankFast', [210, 190], 0.0, 0.0, 10.0, [])
        closet_tank = origin_tank.get_closest_dist_tank(test_target_tanks)
        self.assertEquals(closet_tank, (14.142135623730951, tank_3))

        origin_tank = Tank('origin_tank', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        closet_tank = origin_tank.get_closest_dist_tank(test_target_tanks)
        self.assertEquals(closet_tank, (0.0, tank_2))

        origin_tank = Tank('origin_tank', 100.0, 2.0, 2.0, 'TankFast', [999, 999], 0.0, 0.0, 10.0, [])
        closet_tank = origin_tank.get_closest_dist_tank(test_target_tanks)
        self.assertEquals(closet_tank, (988.5352800987935, tank_4))

    def test_get_radians_to_tank(self):
        tank_1 = Tank('tank_1', 100.0, 2.0, 2.0, 'TankFast', [0, 0], 0.0, 0.0, 10.0, [])
        tank_2 = Tank('tank_2', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        # 45 degrees CCW
        self.assertAlmostEquals(tank_1.get_rads_to_tank(tank_2), 0.785398163397)
        # 135 degrees CW
        self.assertAlmostEquals(tank_2.get_rads_to_tank(tank_1), -2.35619449019)

    def test_get_point_track_to_tank(self):
        tank_1 = Tank('tank_1', 100.0, 2.0, 2.0, 'TankFast', [0, 0], 0.0, 0.0, 10.0, [])
        tank_2 = Tank('tank_2', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        # 45 degrees CCW
        self.assertEquals(tank_1.get_direction_rotation_track_to_tank(tank_2), ('CCW', 0.7853981633974483))
        # 135 degrees CW
        self.assertEquals(tank_2.get_direction_rotation_track_to_tank(tank_1), ('CW', 2.356194490192345))

    def test_get_point_turret_to_tank(self):
        tank_1 = Tank('tank_1', 100.0, 2.0, 2.0, 'TankFast', [0, 0], 0.0, 0.0, 10.0, [])
        tank_2 = Tank('tank_2', 100.0, 2.0, 2.0, 'TankFast', [100, 100], 0.0, 0.0, 10.0, [])
        # 45 degrees CCW
        self.assertEquals(tank_1.get_direction_rotation_turret_to_tank(tank_2), ('CCW', 0.7853981633974483))
        # 135 degrees CW
        self.assertEquals(tank_2.get_direction_rotation_turret_to_tank(tank_1), ('CW', 2.356194490192345))

    def test_line_intersect(self):
        algo = Algorithm('testclient', 'pseudo_client_token')
        # vertical lines, no overlap
        self.assertFalse(algo.line_intersect(
            [10, 10, 10, 50],
            [20, 10, 20, 50]
        ))
        # vertical lines, no overlap
        self.assertFalse(algo.line_intersect(
            [10, 10, 10, 50],
            [10, 60, 10, 90]
        ))
        # vertical overlapping all
        self.assertTrue(algo.line_intersect(
            [10, 10, 10, 50],
            [10, 10, 10, 50]
        ))
        # vertical overlapping partial
        self.assertTrue(algo.line_intersect(
            [10, 10, 10, 50],
            [10, 40, 10, 80]
        ))

        # horizontal lines, no overlap
        self.assertFalse(algo.line_intersect(
            [10, 10, 50, 10],
            [10, 20, 50, 20]
        ))
        # no overlap
        self.assertFalse(algo.line_intersect(
            [10, 10, 50, 10],
            [60, 10, 90, 10]
        ))
        # overlapping all
        self.assertTrue(algo.line_intersect(
            [10, 10, 50, 10],
            [10, 10, 50, 10]
        ))
        # overlapping partial
        self.assertTrue(algo.line_intersect(
            [10, 10, 50, 10],
            [40, 10, 80, 10]
        ))

        # non-parallel overlap
        self.assertTrue(algo.line_intersect(
            [10, 10, 20, 30],
            [10, 30, 20, 20]
        ))

        # non-parallel no overlap
        self.assertFalse(algo.line_intersect(
            [10, 10, 20, 20],
            [30, 30, 21, 21]
        ))

        
if __name__ == '__main__':
    unittest.main()
