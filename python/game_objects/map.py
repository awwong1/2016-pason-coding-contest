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
    nodes = dict()
    adjacency_dictionary = dict()

    def __init__(self, size, obstacles):
        print("Initializing map...")
        m_start = datetime.datetime.now()
        self.size = size
        self.obstacles = obstacles
        self.nodes = dict()
        self.adjacency_dictionary = dict()

        print("Parsing %s number of obstacles..." % str(len(obstacles)))
        for obstacle in obstacles:
            corners = obstacle.to_corners_padding(padding=5)
            for p in corners:
                if self.check_point_in_map(p):
                    node_id = len(self.nodes)
                    self.nodes[node_id] = p
        for node_id, node in self.nodes.iteritems():
            # add edges to the graph between points that are visible to one another
            p1 = node
            for node2_id, node2 in self.nodes.iteritems():
                p2 = node2
                if node_id == node2_id:
                    continue  # no edge to itself
                # check if p1 and p2 are visible to one-another
                visible = True
                for obstacle in obstacles:
                    edges = obstacle.to_edges()
                    for e in edges:
                        if Map.line_intersect(p1 + p2, e):
                            visible = False
                            break
                    if not visible:
                        break
                if visible:
                    d = Map.get_euclidean_dist(p1, p2)
                    if node_id not in self.adjacency_dictionary:
                        self.adjacency_dictionary[node_id] = dict()
                        if node2_id not in self.adjacency_dictionary[node_id]:
                            self.adjacency_dictionary[node_id][node2_id] = dict()
                    self.adjacency_dictionary[node_id][node2_id] = d
                    if node2_id not in self.adjacency_dictionary:
                        self.adjacency_dictionary[node2_id] = dict()
                        if node_id not in self.adjacency_dictionary[node2_id]:
                            self.adjacency_dictionary[node2_id][node_id] = dict()
                    self.adjacency_dictionary[node2_id][node_id] = d
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

    def dijkstra(self, source_node, dest_node):
        # based on: http://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
        # and wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        prev = {node_id: None for node_id in self.nodes.keys()}
        unvisited = {node_id: None for node_id in self.nodes.keys()}
        current_node_id = None
        for node_id, node in self.nodes.iteritems():
            if node == source_node:
                current_node_id = node_id
                break
        current_distance = 0
        if current_node_id is None:
            return []
        unvisited[current_node_id] = current_distance

        while True:
            for neighbour_id, neighbour_dist in self.adjacency_dictionary[current_node_id].iteritems():
                if (neighbour_dist + 0.0) < EPSILON:
                    continue
                if neighbour_id not in unvisited:
                    continue
                new_distance = current_distance + neighbour_dist
                if unvisited[neighbour_id] is None or unvisited[neighbour_id] > new_distance - EPSILON:
                    unvisited[neighbour_id] = new_distance
                    prev[neighbour_id] = current_node_id
            del unvisited[current_node_id]
            if not unvisited:
                break
            candidates = [c_node for c_node in unvisited.iteritems() if c_node[1]]
            if not candidates:
                break
            current_node_id, current_distance = sorted(candidates, key=lambda x: x[1])[0]

        path = []
        last_node = dest_node
        last_node_id = None
        for node_id, node in self.nodes.iteritems():
            if node == last_node:
                last_node_id = node_id
                break
        if last_node_id in prev and prev[last_node_id] is not None:
            path.append(last_node)
        while last_node_id in prev and prev[last_node_id] is not None:
            path.append(prev[last_node_id])
            last_node_id = prev[last_node_id]
        path.reverse()
        return path

    def get_path(self, tank, enemy):
        """
        Given a tank and a target. Return the location which the tank should move to.
        :param tank: a friendly tank
        :param enemy: the enemy which tank is targeting
        """
        (enemy_dist, enemy_node) = self.get_closest_dist_node(enemy)
        (our_dist, our_node) = self.get_closest_dist_node(tank)
        print("Tank: %s" % tank.id)
        print(our_dist)
        print(our_node)
        path = self.dijkstra(our_node, enemy_node)
        if not path:
            return 0, 0, 0  # todo find new target
        if tank.last_node is None:
            # goto first node
            dest_node = path[0]
            dest_cord = self.nodes[dest_node]
            tra_dir, tra_rad = tank.get_direction_rotation_track_to_point(dest_cord)
            if self.get_euclidean_dist(tank.position, dest_cord) < 5:
                tank.last_node = dest_node
        else:
            if path[0] is not tank.last_node:
                # the tank has passed the first node
                # we recompute the path, the path no longer contains the original first node
                dest_node = path[0]
                tank.last_node = None
            else:
                # go to next node
                dest_node = path[1]
            dest_cord = self.nodes[dest_node]
            tra_dir, tra_rad = tank.get_direction_rotation_track_to_point(dest_cord)
            if self.get_euclidean_dist(tank.position, dest_cord) < 5:
                tank.last_node = dest_node
        dist = tank.get_dist_to_point(dest_cord)
        return dist, tra_dir, tra_rad

    def get_all_dist_node(self, tank):
        """
        Given a tank as a parameter, return a list of (dist, node) tuples sorted by distance increasing
        :param tank: a tank
        :return: [(Distance, Node)]. Empty array if no nodes
        """
        dists_and_nodes = []
        if self.nodes:
            for node_id, node in self.nodes.iteritems():
                dist = math.hypot(tank.position[0] - node[0], tank.position[1] - node[1])
                dists_and_nodes.append((dist, node))
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


class Graph:
    nodes = []  # list of node id's
    node_coordinates = dict()  # id to list
    edges = []  # list of lists

    def __init__(self):
        pass
