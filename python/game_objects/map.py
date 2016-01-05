import datetime
import math

EPSILON = 1e-6


class Map:
    """
    Map origin (0, 0) is bottom left
    size (Integer Tuple)
    * The width and height, in metres, of the game map (In that order).
    obstacles (Obstacle Array)
    """
    size = []
    obstacles = []
    node_list = []
    node_positions = []
    adjacency_matrix = []

    def __init__(self, size, obstacles):
        print("Initializing map...")
        m_start = datetime.datetime.now()
        self.size = size
        self.obstacles = obstacles
        self.node_list = []  # node ids
        self.node_positions = []  # list of 2-element lists
        self.adjacency_matrix = []  # value > 0.0 + EPSILON means an edge exists

        print("Parsing %s number of obstacles..." % str(len(obstacles)))
        for obstacle in obstacles:
            corners = obstacle.to_corners_padding(padding=1)
            for p in corners:
                if self.check_point_in_map(p):
                    node_id = len(self.node_list)
                    self.node_list.append(node_id)
                    self.node_positions.append(p)
        # have all the nodes, can construct empty edge graph
        for _ in self.node_list:
            self.adjacency_matrix.append([])
            for _2 in self.node_list:
                self.adjacency_matrix[-1].append(0.0)
        for node_id in self.node_list:
            # add edges to the graph between points that are visible to one another
            p1 = self.node_positions[node_id]
            for node2_id in self.node_list:
                p2 = self.node_positions[node2_id]
                if node_id == node2_id:
                    continue  # no edge to itself
                # check if p1 and p2 are visible to one-another
                for obstacle in obstacles:
                    edges = obstacle.to_edges()
                    visible = True
                    for e in edges:
                        if Map.line_intersect(p1 + p2, e):
                            visible = False
                    if not visible:
                        continue
                    else:
                        d = Map.get_euclidean_dist(p1, p2)
                        self.adjacency_matrix[node_id][node2_id] = d
                        self.adjacency_matrix[node2_id][node_id] = d
        # we should color the connected graph components
        # So, each node will have the same colour as all the nodes which it can reach.
        # then if we are checking if a tank can reach another, we can see what colour nodes the tanks can reach
        """
        current_color = 0
        for node in self.adjacency_list:
            if node.colour > 0:
                continue
            # we have a new node that has not been visited before. Make a new colour
            current_color += 1
            queue = []
            for i in node.neighbours:
                if self.adjacency_list[i].colour == 0:
                    self.adjacency_list[i].colour = -1  # colour tracked nodes
                    queue.append(i)

            while queue:  # non-empty
                node_index = queue.pop()
                p_node = self.adjacency_list[node_index]
                if not p_node:
                    print("failed to find neighbour!")
                if p_node.colour > 0:
                    continue  # visited this node and its neighbours already
                for i in p_node.neighbours:
                    if self.adjacency_list[i].colour == 0:
                        self.adjacency_list[i].colour = -1  # colour tracked nodes
                        queue.append(i)
                p_node.colour = current_color
        print("current colors: {}".format(current_color))
        """
        # should this algorithm compute the shortest paths between all nodes?
        m_end = datetime.datetime.now()
        m_diff = m_end - m_start
        print("Map initialization finished, took %s seconds" % str(m_diff.total_seconds()))

    def __eq__(self, other):
        return self.size == other.size and str(sorted(self.obstacles)) == str(sorted(other.obstacles))

    def __str__(self):
        return "<Map>: %s; %s" % (str(self.size), str(self.obstacles))

    def __repr__(self):
        return "<Map>: %s; %s" % (str(self.size), str(self.obstacles))

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        a = str(self)
        b = str(other)
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    @staticmethod
    def line_intersect(line_1, line_2):
        """
        Determine if two lines intersect
        https://www.topcoder.com/community/data-science/data-science-tutorials/
        geometry-concepts-line-intersection-and-its-applications/

        :param line_1: Array of four points, [x_0, y_0, x_1, y_1]
        :param line_2: Array of four points, [x_0, y_0, x_1, y_1]
        :return: Boolean, true if line intersects, false otherwise
        """
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

    def check_point_in_map(self, point):
        if ((0 - EPSILON < point[0]) and (self.size[0] + EPSILON > point[0]) and
                (0 - EPSILON < point[1]) and (self.size[1] + EPSILON > point[1])):
            return True
        else:
            return False

    @staticmethod
    def get_euclidean_dist(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def dijkstra(self, adj_mat, source, dest):
        # based on: http://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
        # and wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        prev = {node: None for node in self.node_list}  # using None as +inf
        unvisited = {node: None for node in self.node_list}  # using None as +inf
        current = source
        current_distance = 0
        unvisited[current] = current_distance

        while True:
            for neighbour_id, neighbour_dist in enumerate(adj_mat[current]):
                if (neighbour_dist + 0.0) < EPSILON:
                    continue
                if neighbour_id not in unvisited:
                    continue
                new_distance = current_distance + neighbour_dist
                if unvisited[neighbour_id] is None or unvisited[neighbour_id] > new_distance - EPSILON:
                    unvisited[neighbour_id] = new_distance
                    prev[neighbour_id] = current
            del unvisited[current]
            if not unvisited:
                break
            candidates = [node for node in unvisited.items() if node[1]]
            current, current_distance = sorted(candidates, key=lambda x: x[1])[0]

        path = []
        last_node = dest
        if prev[dest] is not None:
            path.append(dest)
        while prev[last_node] is not None:
            path.append(prev[last_node])
            last_node = prev[last_node]
        path.reverse()
        return path

    def get_path(self, tank, enemy):
        """
        Given a tank and a target. Return the location which the tank should move to.
        :param tank: a friendly tank
        :param enemy: the enemy which tank is targeting
        """
        (enemy_dist, enemy_node_id) = self.get_closest_dist_node(enemy)
        (our_dist, our_node_id) = self.get_closest_dist_node(tank)
        """
        if (enemy_node.color != our_node.color):
            # the enemy tank is not reachable
            # TODO figure out what to do when this occurs
            pass
        """

        # if tank is a new tank -- find a path from our_node to enemy_node -- using Dijkstra's algorithm?
        if not tank.path:
            # store a list of the node id's on the path in the tank
            path = self.dijkstra(self.adjacency_matrix, our_node_id, enemy_node_id)
            tank.path = path
            # print tank.path
            if not path:
                return 0, 0, 0  # todo find new target
            # goto first node
            dest_node = tank.path[0]
            dest_cord = self.node_positions[dest_node]
            tra_dir, tra_rad = tank.get_direction_rotation_track_to_point(dest_cord)
            # todo return the movement command?
            dist = tank.get_dist_to_point(dest_cord)
            return dist, tra_dir, tra_rad
        elif len(tank.path) > 1:  # uses [-1] to denote end of path
            # existing tank -- continue on the existing path if the enemy exists
            # while the tank is not at the first node id -- move to that node
            # if the node is at the first id, remove it from the list and proceed to the next node on the map.
            dest_node = tank.path[0]
            dest_cord = self.node_positions[dest_node]
            dist = tank.get_dist_to_point(dest_cord)
            if dist < EPSILON:
                del tank.path[0]
                # TODO check if tank.path[0] == -1, then the tank is at the node closest to the enemy
                # otherwise drive the tank to the next node
                return self.get_path(tank, enemy)
            else:
                tra_dir, tra_rad = tank.get_direction_rotation_track_to_point(dest_cord)
                # todo return the movement command?
                return dist, tra_dir, tra_rad
        else:
            # if there are no more nodes, the tank has arrived at the node closest to the enemy location
            tra_dir, tra_rad = tank.get_direction_rotation_track_to_tank(enemy)
            # todo return the movement command?
            dist = tank.get_dist_to_point(enemy.position)
            return dist, tra_dir, tra_rad

    def get_all_dist_node(self, tank):
        """
        Given a tank as a parameter, return a list of (dist, node) tuples sorted by distance increasing
        :param tank: a tank
        :return: [(Distance, Node)]. Empty array if no nodes
        """
        dists_and_nodes = []
        if self.node_list:
            for node_id in self.node_list:
                point = self.node_positions[node_id]
                dist = math.hypot(tank.position[0] - point[0], tank.position[1] - point[1])
                dists_and_nodes.append((dist, node_id))
        return sorted(dists_and_nodes)

    def get_closest_dist_node(self, tank):
        """
        Given a tank as a parameter, return the closest map node.
        :param tank:  a tank
        :return: Distance, Node. None if no nodes.
        """
        dist_nodes = self.get_all_dist_node(tank)
        if dist_nodes:
            return dist_nodes[0]
        return None


class Node:
    index = -1
    point = []
    neighbours = []  # index into a list of nodes
    colour = 0

    def __init__(self, point):
        self.point = point

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)


class Graph:
    nodes = []  # list of node id's
    node_coordinates = dict()  # id to list
    edges = []  # list of lists

    def __init__(self):
        pass
