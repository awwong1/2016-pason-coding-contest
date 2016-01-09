from command import Command, CommType
from game_objects.map import Map
from game_objects.obstacle import Obstacle
from game_objects.player import Player
from game_objects.projectile import Projectile
from game_objects.tank import Tank


class Algorithm:
    """
    Calculates the actions for the current game state.
    """
    team_name = ""
    client_token = ""
    time_remaining = ""
    map = None
    players = []

    def __init__(self, team_name, client_token):
        self.team_name = team_name
        self.client_token = client_token

    def parse_game_state(self, json_game_state, parse_map=False):
        """
        json_game_state structure
        Populate self with the json_game_state.
        :param json_game_state: Json object of the current game state
        """
        self.time_remaining = json_game_state['timeRemaining']
        if parse_map:
            map_size = json_game_state['map']['size'][0], json_game_state['map']['size'][1]
            map_obstacles = []
            for terrain in json_game_state['map']['terrain']:
                map_obstacles.append(
                    Obstacle(terrain['type'], terrain['boundingBox']['corner'], terrain['boundingBox']['size'])
                )
            self.map = Map(map_size, map_obstacles)

        self.players = []
        for player in json_game_state['players']:
            score = player['score']
            name = player['name']
            tanks = []
            for tank in player['tanks']:
                id = tank['id']
                health = tank['health']
                hit_radius = tank['hitRadius']
                collision_radius = tank['collisionRadius']
                type = tank['type']
                position = tank['position']
                tracks = tank['tracks']
                turret = tank['turret']
                speed = tank['speed']
                projectiles = []
                for projectile in tank['projectiles']:
                    p_id = projectile['id']
                    p_position = projectile['position']
                    p_direction = projectile['direction']
                    p_speed = projectile['speed']
                    p_damage = projectile['damage']
                    p_range = projectile['range']
                    projectiles.append(Projectile(p_id, p_position, p_direction, p_speed, p_damage, p_range))
                tanks.append(
                    Tank(id, health, hit_radius, collision_radius, type, position, tracks, turret, speed, projectiles))
            self.players.append(Player(name, score, tanks))

    def generate_actions(self):
        actions = []
        my_player = None
        enemy_player = None

        for player in self.players:
            if player.name == self.team_name:
                my_player = player
            else:
                enemy_player = player

        for my_tank in my_player.tanks:
            # slooow, currently this basically doesn't run. Takes ~10-20 seconds per a-star search per tank
            print "Calculating for %s" % my_tank.id
            s_path = []
            s_path_tank = None
            closest_tank = None
            closest_tank_dist = None
            for enemy_dist, enemy_tank in my_tank.get_all_dist_tank(enemy_player.tanks):
                if closest_tank is None:
                    closest_tank = enemy_tank
                    closest_tank_dist = enemy_dist
                print "\t %s" % enemy_tank.id
                temp_s_path = self.map.get_shortest_path(my_tank.position, enemy_tank.position)
                if len(temp_s_path) > 0:
                    s_path = temp_s_path
                    s_path_tank = enemy_tank
                    break
            if s_path_tank is not None:
                print "\t Going to wreck %s" % s_path_tank.id
                print "\t" + str(s_path)
                tur_dir, tur_rad = my_tank.get_direction_rotation_turret_to_tank(s_path_tank)
                tra_dir, tra_rad = my_tank.get_direction_rotation_track_to_point(s_path[0])
                dist = my_tank.get_dist_to_point(s_path_tank.position)
                actions.append(Command.get_turret_rotation_command(my_tank.id, tur_dir, tur_rad, self.client_token))
                actions.append(Command.get_tank_rotation_command(my_tank.id, tra_dir, tra_rad, self.client_token))
                actions.append(Command.get_movement_command(my_tank.id, 'FWD', my_tank.get_dist_to_point(s_path[0]),
                                                            self.client_token))
                if my_tank.no_friendly_fire(my_player.tanks, dist, s_path_tank):
                    actions.append(Command.get_fire_command(my_tank.id, self.client_token))
                else:
                    # don't shoot friend from queued bullet
                    actions.append(Command.get_stop_command(my_tank.id, CommType.FIRE, self.client_token))
            else:
                print "\t Pathing failed, just locking on closest enemy tank"
                tur_dir, tur_rad = my_tank.get_direction_rotation_turret_to_tank(closest_tank)
                actions.append(Command.get_turret_rotation_command(my_tank.id, tur_dir, tur_rad, self.client_token))
                if my_tank.no_friendly_fire(my_player.tanks, closest_tank_dist, closest_tank):
                    actions.append(Command.get_fire_command(my_tank.id, self.client_token))
                else:
                    actions.append(Command.get_stop_command(my_tank.id, CommType.FIRE, self.client_token))
            """
            dist, tank = my_tank.get_closest_dist_tank(enemy_player.tanks)
            tur_dir, tur_rad = my_tank.get_direction_rotation_turret_to_tank(tank)
            tra_dir, tra_rad = my_tank.get_direction_rotation_track_to_tank(tank)
            actions.append(Command.get_turret_rotation_command(my_tank.id, tur_dir, tur_rad, self.client_token))
            actions.append(Command.get_tank_rotation_command(my_tank.id, tra_dir, tra_rad, self.client_token))
            actions.append(Command.get_movement_command(my_tank.id, 'FWD', dist, self.client_token))
            if my_tank.no_friendly_fire(my_player.tanks, dist, tank):
                actions.append(Command.get_fire_command(my_tank.id, self.client_token))
            else:
                # don't shoot friend from queued bullet
                actions.append(Command.get_stop_command(my_tank.id, CommType.FIRE, self.client_token))
            """
        return actions
