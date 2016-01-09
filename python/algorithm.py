from command import Command
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

    def parse_game_state(self, json_game_state):
        """
        json_game_state structure
        Populate self with the json_game_state.
        :param json_game_state: Json object of the current game state
        """
        self.time_remaining = json_game_state['timeRemaining']
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

        # let's do this the dumbest way possible, all at once
        for my_tank in my_player.tanks:
            dist, tank = my_tank.get_closest_tank(enemy_player.tanks)
            tur_dir, tur_rad = my_tank.get_point_turret_to_tank(tank)
            tra_dir, tra_rad = my_tank.get_point_track_to_tank(tank)
            actions.append(Command.get_turret_rotation_command(my_tank.id, tur_dir, tur_rad, self.client_token))
            actions.append(Command.get_tank_rotation_command(my_tank.id, tra_dir, tra_rad, self.client_token))
            actions.append(Command.get_movement_command(my_tank.id, 'FWD', dist, self.client_token))

            if my_tank.is_friendly_fire(my_player.tanks, my_tank.get_dist_to_tank(tank), tank):
                # don't shoot friend from queued bullet
                actions.append(Command.get_stop_command(my_tank.id, 'FIRE', self.client_token))
            else:
                actions.append(Command.get_fire_command(my_tank.id, self.client_token))
            # actions.append(Command.get_fire_command(my_tank.id, self.client_token))
        return actions
