class Projectile:
    """
    Projectile Object
    id (String)
    * The UUID that is generated at the creation of the projectile object.
    position (Array of Numbers)
    * The coordinates, in metres, of the projectile on the map.
    direction (Number)
    * The angle, in radians, of travel for the projectile relative to the (1,0) unit vector.
    speed (Number)
    * The speed, in m/s, at which the projectile is traveling at.
    damage (Number)
    The damage this projectile is capable of inflicting on a tank in health units.
    range (Number)
    * The range that this projectile will travel until it expires.
    """
    # Maximum range might be 50 meters (however event loop only sees a max of 47)
    # Speed is 30.0 meters per second
    # Damage is 100.0 damage
    id = ""
    position = []
    direction = None
    speed = None
    damage = None
    range = None

    def __init__(self, id, position, direction, speed, damage, range):
        self.id = id
        self.position = position
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.range = range

    def __eq__(self, other):
        return self.id == other.id and self.position == other.position and self.direction == other.direction and \
               self.speed == other.speed and self.damage == other.damage and self.range == other.range

    def __str__(self):
        return "<Projectile>: %s; position %s; direction %s; speed %s; damage %s; range %s" % (
            self.id, str(self.position), self.direction, self.speed, self.damage, self.range
        )

    def __repr__(self):
        return "<Projectile>: %s; position %s; direction %s; speed %s; damage %s; range %s" % (
            self.id, str(self.position), self.direction, self.speed, self.damage, self.range
        )

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
