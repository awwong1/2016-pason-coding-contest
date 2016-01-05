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

    def to_edges(self):
        width, height = self.size
        bl_corner = self.corner
        br_corner = [bl_corner[0] + width, bl_corner[1]]
        ul_corner = [bl_corner[0], bl_corner[1] + height]
        ur_corner = [bl_corner[0] + width, bl_corner[1] + height]
        edges = [bl_corner + br_corner, bl_corner + ul_corner, ul_corner + ur_corner, br_corner + ur_corner]
        return edges

    def to_corners(self):
        width, height = self.size
        bl_corner = self.corner
        br_corner = [bl_corner[0] + width, bl_corner[1]]
        ul_corner = [bl_corner[0], bl_corner[1] + height]
        ur_corner = [bl_corner[0] + width, bl_corner[1] + height]
        corners = [bl_corner, br_corner, ul_corner, ur_corner]
        return corners

    def to_edges_padding(self, padding=5):
        width, height = self.size
        bl_corner = self.corner
        # how big should padding be so tank doesn't hit wall
        br_corner = [bl_corner[0] + width + padding, bl_corner[1] - padding]
        ul_corner = [bl_corner[0] - padding, bl_corner[1] + height + padding]
        ur_corner = [bl_corner[0] + width + padding, bl_corner[1] + height + padding]
        bl_corner = [bl_corner[0] - padding, bl_corner[1] - padding]
        edges = [bl_corner + br_corner, bl_corner + ul_corner, ul_corner + ur_corner, br_corner + ur_corner]
        return edges

    def to_corners_padding(self, padding=5):
        width, height = self.size
        bl_corner = self.corner
        # how big should padding be so tank doesn't hit wall
        br_corner = [bl_corner[0] + width + padding, bl_corner[1] - padding]
        ul_corner = [bl_corner[0] - padding, bl_corner[1] + height + padding]
        ur_corner = [bl_corner[0] + width + padding, bl_corner[1] + height + padding]
        bl_corner = [bl_corner[0] - padding, bl_corner[1] - padding]
        corners = [bl_corner, br_corner, ul_corner, ur_corner]
        return corners
