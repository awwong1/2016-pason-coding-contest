import numpy
from heapq import heappop, heappush


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
    RESOLUTION = 10
    size = []
    obstacles = []
    col_grid = numpy.array([])
    grid = []

    def __init__(self, size, obstacles):
        self.size = size
        self.obstacles = obstacles

        # Create the grid for pathfinding purposes.
        # NOTE: If any obstacles overlap, later obstacles will overwrite newer obstacles.
        self.col_grid = numpy.array(
                [[0 for y in range(size[1] / Map.RESOLUTION)] for x in range(size[0] / Map.RESOLUTION)])
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
                        self.col_grid[(origin_x + writer_x) / Map.RESOLUTION][
                            (origin_y + writer_y) / Map.RESOLUTION] = 1
                        self.grid[origin_x + writer_x][origin_y + writer_y] = terrain_type
                    except IndexError:
                        # Obstacles seem to be able to extend past the map
                        pass
        print self.get_mod_10_grid_display()

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

    def get_mod_10_grid_display(self):
        """
        Get a string which represents the map as it would appear in the visualizer.
        Seems like every object on screen is 10m by 10m, so this displays it nicer and fits better in terminal stdout
        :return: String, visualized representation of the grid
        """
        v_grid = ""
        for row in zip(*zip(*zip(*self.grid[::-1])[::-1])[::-1]):
            v_grid += "".join(map(str, row[0::10])) + "\n"
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
                        flat_data.append((data[i - 1][0] * Map.RESOLUTION, data[i - 1][1] * Map.RESOLUTION))
                        delta = p_delta
                if not flat_data and data:
                    flat_data = [(data[-1][0] * Map.RESOLUTION, data[-1][1] * Map.RESOLUTION), ]
                elif flat_data:
                    flat_data.append((r_goal[0] * Map.RESOLUTION, r_goal[1] * Map.RESOLUTION))
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
