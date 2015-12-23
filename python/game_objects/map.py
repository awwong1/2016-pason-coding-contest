class Map:
    """
    Map origin (0, 0) is bottom left
    size (Integer Tuple)
    * The width and height, in metres, of the game map (In that order).
    obstacles (Obstacle Array)
    * Array of obstacles on the map
    grid (2D Matrix)
    * Representation of the map wrt map coordinates numbering.
    * (0 - No obstacle, 1 - Impassable, 2 - Solid)
    * NOTES: grid[0][0] is the bottom left of the actual game map. Simply pass in your given [X] and [Y].
      Use the 'get_grid_display' to display the map as it would appear in the visualizer. (Debugging purposes)
    """
    size = []
    obstacles = []
    grid = []

    def __init__(self, size, obstacles):
        self.size = size
        self.obstacles = obstacles

        # Create the grid for pathfinding purposes.
        # NOTE: If any obstacles overlap, later obstacles will overwrite newer obstacles.
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
