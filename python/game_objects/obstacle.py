class Obstacle:
    """
    Bounding box obstacle.
    obs_type (String)
    * Describes the type of terrain object it is (i.e SOLID or IMPASSABLE).
    corner (Integer Array)
    * The coordinates, in metres, of the corner of the terrain closest to the map origin. (Bottom left)
    size (Integer Array)
    * The width and height, in metres, of the terrain object (in that order).
    """
    corner = []
    size = []
    type = ""

    def __init__(self, obs_type, corner, size):
        self.type = obs_type
        self.corner = corner
        self.size = size

    def __eq__(self, other):
        return self.type == other.type and self.corner == other.corner and self.size == other.size

    def __str__(self):
        return "<Obstacle> %s; corner: %s; size: %s" % (self.type, self.corner, self.size)

    def __repr__(self):
        return "<Obstacle> %s; corner: %s; size: %s" % (self.type, self.corner, self.size)

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
