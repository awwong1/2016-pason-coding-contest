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
        print("parsing obstacles.")
        self.map.parse_game_state(map_obstacles, map_size, self)
        print("end parsing obstacles.")

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
                        Tank(id, health, hit_radius, collision_radius, type, position, tracks, turret, speed,
                             projectiles))
            self.players.append(Player(name, score, tanks))

    def line_intersect(self, line_1, line_2):
        EPSILON = 1e-6
        # line_1 = [x_0, y_0, x_1, y_1]
        # https://www.topcoder.com/community/data-science/data-science-tutorials/geometry-concepts-line-intersection-and-its-applications/
        a1 = line_1[3] - line_1[1]
        b1 = line_1[0] - line_1[2]
        c1 = a1 * line_1[0] + b1 * line_1[1]

        a2 = line_2[3] - line_2[1]
        b2 = line_2[0] - line_2[2]
        c2 = a2 * line_2[0] + b2 * line_2[1]

        det = a1 * b2 - a2 * b1
        if abs(det) < EPSILON:  # parallel
            # partial horizontal overlap
            if abs(line_1[1] - line_2[1]) < EPSILON:
                x1 = line_2[0]
                x2 = line_2[2]
                if min(line_1[0], line_1[2]) - EPSILON < x1 < EPSILON + max(line_1[0], line_1[2]):
                    return True
                if min(line_1[0], line_1[2]) - EPSILON < x2 < EPSILON + max(line_1[0], line_1[2]):
                    return True
            # partial vertical overlap
            if abs(line_1[0] - line_2[0]) < EPSILON:
                y1 = line_2[1]
                y2 = line_2[3]
                if ((min(line_1[1], line_1[3]) - EPSILON < y1) and
                        (max(line_1[1], line_1[3]) + EPSILON > y1)):
                    return True
                if ((min(line_1[1], line_1[3]) - EPSILON < y2) and
                        (max(line_1[1], line_1[3]) + EPSILON > y2)):
                    return True
            # no overlap
            return False
        else:
            x = (b2 * c1 - b1 * c2) / det
            y = (a1 * c2 - a2 * c1) / det

            if (min(line_1[0], line_1[2]) - EPSILON < x and  # point is on
                            max(line_1[0], line_1[2]) + EPSILON > x and  # the first line
                            min(line_1[1], line_1[3]) - EPSILON < y and
                            max(line_1[1], line_1[3]) + EPSILON > y and
                            min(line_2[0], line_2[2]) - EPSILON < x and  # point is on
                            max(line_2[0], line_2[2]) + EPSILON > x and  # the 2nd line
                            min(line_2[1], line_2[3]) - EPSILON < y and
                            max(line_2[1], line_2[3]) + EPSILON > y):
                return True
            else:
                return False

    def generate_tank_path(self, my_tank, enemy_tank, dist):
        x_0, y_0 = my_tank.position
        x_1, y_1 = enemy_tank.position

        # determine what color the tanks are if there is an obstruction
        # closest map node
        my_node = self.map.get_closest_dist_node(
            my_tank)  # this node should be reachable by the tank because it is the closest unobstructed point
        enemy_node = self.map.get_closest_dist_node(enemy_tank)  # same here
        # the tanks should have the same color as these nodes

        # find a path from my_node to enemy_node in self.map.map
        # TODO implement DFS on adjacency list of self.map.map

        obstacles = self.map.obstacles
        for obstacle in obstacles:
            edges = obstacle.to_edges_padding()
            for e in edges:
                if self.line_intersect([x_0, y_0, x_1, y_1], e):
                    # drive to one of the points from the line that is obstructing the tank
                    point = []
                    if enemy_tank.get_dist_to_point([e[0], e[1]]) < enemy_tank.get_dist_to_point([e[2], e[3]]):
                        point = [e[0], e[1]]
                    else:
                        point = [e[2], e[3]]
                    # just pick the first point in the edge for now?
                    # this isn't even gauranteed to be the closest edge
                    tra_dir, tra_rad = my_tank.get_direction_rotation_track_to_point(point)
                    dist = my_tank.get_dist_to_point([e[0], e[1]])
                    return [tra_dir, tra_rad, dist]

        tra_dir, tra_rad = my_tank.get_direction_rotation_track_to_tank(enemy_tank)
        return [tra_dir, tra_rad, dist]

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
            """
            # slooow, currently this basically doesn't run. Takes ~10-20 seconds per a-star search per tank
            print "Calculating for %s" % my_tank.id
            s_path_len = float('inf')
            s_path = []
            s_path_tank = None

            for enemy_tank in enemy_player.tanks:
                print "\t %s" % enemy_tank.id
                temp_s_path = self.map.get_shortest_path(my_tank.position, enemy_tank.position)
                if s_path_len > len(temp_s_path) > 0:
                    s_path_len = len(temp_s_path)
                    s_path = temp_s_path
                    s_path_tank = enemy_tank
            if s_path_tank is not None:
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
            """
            dist, tank = my_tank.get_closest_dist_tank(enemy_player.tanks)
            tur_dir, tur_rad = my_tank.get_direction_rotation_turret_to_tank(tank)
            tra_dir, tra_rad = my_tank.get_direction_rotation_track_to_tank(tank)

            dist, tra_dir, tra_rad = self.map.get_path(my_tank, tank)
            actions.append(Command.get_turret_rotation_command(my_tank.id, tur_dir, tur_rad, self.client_token))
            # tra_dir, tra_rad, dist = self.generate_tank_path(my_tank, tank, dist)  # use naive method until the pathing works

            actions.append(Command.get_tank_rotation_command(my_tank.id, tra_dir, tra_rad, self.client_token))
            # todo don't run over ally
            actions.append(Command.get_movement_command(my_tank.id, 'FWD', dist, self.client_token))
            if my_tank.no_friendly_fire(my_player.tanks, dist, tank):
                actions.append(Command.get_fire_command(my_tank.id, self.client_token))
            else:
                # don't shoot friend from queued bullet
                actions.append(Command.get_stop_command(my_tank.id, CommType.FIRE, self.client_token))
        return actions
