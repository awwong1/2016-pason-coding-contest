import numpy
import math
from heapq import heappop, heappush

EPSILON = 1e-6


class Map:
    """
    Map origin (0, 0) is bottom left
    size (Integer Tuple)
    * The width and height, in metres, of the game map (In that order).
    obstacles (Obstacle Array)
    * Array of obstacles on the map
    col_grid (numpy.array)
    * Representation of the map wrt map coordinates numbering for a-star search.
    * (0 - No obstacle, 1 - Obstacle)
    grid (2D Matrix)
    * Representation of the map wrt map coordinates numbering.
    * (0 - No obstacle, 1 - Impassable, 2 - Solid)
    * NOTES: grid[0][0] is the bottom left of the actual game map. Simply pass in your given [X] and [Y].
      Use the 'get_grid_display' to display the map as it would appear in the visualizer. (Debugging purposes)
    """
    size = []
    obstacles = []
    col_grid = numpy.array([])
    grid = []

    def __init__(self, size, obstacles):
        self.size = size
        self.obstacles = obstacles

        # Create the grid for pathfinding purposes.
        # NOTE: If any obstacles overlap, later obstacles will overwrite newer obstacles.
        self.col_grid = numpy.array([[0 for y in range(size[1])] for x in range(size[0])])
        self.grid = [[0 for y in range(size[1])] for x in range(size[0])]
        for obstacle in obstacles:
            raw_terrain_type = obstacle.type
            if raw_terrain_type == "NORMAL":
                # Passable by Projectiles and Tanks, equivalent to 0
                continue
            elif raw_terrain_type == "IMPASSABLE":
                terrain_type = 1
            elif raw_terrain_type == "SOLID":
                terrain_type = 2
            else:
                print "Unknown terrain type: %s" % raw_terrain_type
                terrain_type = 9
            origin_x, origin_y = map(int, obstacle.corner)
            size_x, size_y = map(int, obstacle.size)
            for writer_x in xrange(0, size_x):
                for writer_y in xrange(0, size_y):
                    try:
                        self.col_grid[origin_x + writer_x][origin_y + writer_y] = 1
                        self.grid[origin_x + writer_x][origin_y + writer_y] = terrain_type
                    except IndexError:
                        # Obstacles seem to be able to extend past the map
                        pass

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

    def get_grid_display(self):
        """
        Get a string which represents the map as it would appear in the visualizer.
        :return String, visualized representation of the grid
        """
        # http://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        v_grid = ""
        for row in zip(*zip(*zip(*self.grid[::-1])[::-1])[::-1]):
            v_grid += "".join(map(str, row)) + "\n"
        return v_grid

    @staticmethod
    def _heuristic(a, b):
        """
        Heuristic for a-star algorithm
        """
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    def get_shortest_path(self, r_start, r_goal):
        """
        Modified version of astar for our implementation of the map.
        Taken from: Christian Careaga (christian.careaga7@gmail.com) at
        http://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/
        :param r_start (2-list), Integers (x,y) starting position of path
        :param r_goal  (2-list), Integers (x,y) ending position of path
        :return array, empty array if no path. Otherwise every node as (x,y) in path from start to goal.
        """
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        start = tuple(r_start)
        goal = tuple(r_goal)
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: Map._heuristic(start, goal)}
        oheap = []

        heappush(oheap, (fscore[start], start))

        while oheap:
            current = heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                data.reverse()
                # Flatten the points, to be lines (only in eight directions)
                delta = ()
                flat_data = []
                for i in range(0, len(data)):
                    if i == 0:
                        delta = list(a_i - b_i for a_i, b_i in zip(start, data[i]))
                        continue
                    else:
                        p_delta = list(a_i - b_i for a_i, b_i in zip(data[i - 1], data[i]))
                    if p_delta == delta:
                        continue
                    else:
                        flat_data.append(data[i - 1])
                        delta = p_delta
                if not flat_data and data:
                    flat_data = [data[-1]]
                elif flat_data:
                    flat_data.append(r_goal)
                return flat_data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + Map._heuristic(current, neighbor)
                if 0 <= neighbor[0] < self.col_grid.shape[0]:
                    if 0 <= neighbor[1] < self.col_grid.shape[1]:
                        if self.col_grid[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + Map._heuristic(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))

        return []

    def check_point_in_map(self, point):
        if ((0 - EPSILON < point[0]) and (self.size[0] + EPSILON > point[0]) and
                (0 - EPSILON < point[1]) and (self.size[1] + EPSILON > point[1])):
            return True
        else:
            return False

    def parse_game_state(self, obstacles, map_size, algo):
        """
        # todo build a grid for all obstacles when the game is parsed like the current map function.
        # then run dfs or whatever on this grid. It should be smaller than the current one.
        """
        self.adjacency_list = []

        for obstacle in obstacles:
            corners = obstacle.to_corners_padding()
            for p in corners:
                if self.check_point_in_map(p):
                    self.adjacency_list.append(Node(p))  # linked list esque representation
        # add edges to the graph between points that are visible to one another
        for i, node1 in enumerate(self.adjacency_list):
            p1 = node1.point
            p1edges = node1.neighbours
            for j, node2 in enumerate(self.adjacency_list):
                p2 = node2.point
                p2edges = node2.neighbours

                if (i == j):
                    continue  # no edge to itself
                if j in p1edges:
                    continue  # already added a bi-directional edge from p1 to p2
                # check if p1 and p2 are visible to one-another
                for obstacle in obstacles:
                    edges = obstacle.to_edges()
                    visible = True
                    for e in edges:
                        if algo.line_intersect(p1 + p2, e):
                            visible = False
                    if not visible:
                        continue
                    else:
                        node1.add_neighbour(j)
                        node2.add_neighbour(i)
        # we should color the connected graph components
        # So, each node will have the same colour as all the nodes which it can reach.
        # then if we are checking if a tank can reach another, we can see what colour nodes the tanks can reach

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

        # should this algorithm compute the shortest paths between all nodes?

    def get_path(self, tank, enemy):
        """
        Given a tank and a target. Return the location which the tank should move to.
        :param tank: a friendly tank
        :param enemy: the enemy which tank is targeting
        """
        enemy_node = self.get_closest_dist_node(enemy)
        our_node = self.get_closest_dist_node(tank)
        if (enemy_node.color != our_node.color):
            # the enemy tank is not reachable
            # TODO figure out what to do when this occurs
        # if tank is a new tank -- find a path from our_node to enemy_node -- using Dijkstra's algorithm?
            # store a list of the node id's
              # while the tank is not at the first node id -- move to that node
              # if the node is at the first id, remove it from the list and proceed to the next node on the map.
              # if there are no more node, the tank has arrived at the enemy location
        # if tank is an existing tank -- continue on the existing path if the enemy exists
            # do the above
        
    def get_all_dist_node(self, tank):
        """
        Given a tank as a parameter, return a list of (dist, node) tuples sorted by distance increasing
        :param tank: a tank
        :return: [(Distance, Node)]. Empty array if no nodes
        """
        dists_and_nodes = []
        if self.map:
            for node in self.map:
                dist = math.hypot(tank.position[0] - node.point[0], tank.position[1] - node.point[1])
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


class Node:
    point = []
    neighbours = []  # index into a list of nodes
    colour = 0

    def __init__(self, point):
        self.point = point

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
