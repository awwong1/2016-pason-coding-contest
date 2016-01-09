import math


class Tank:
    """
    Tank Object
    id (String)
    * The UUID that is generated at the creation of a tank object (this changes when a tank re-spawns after death).
    health (Integer)
    * The current amount of health units that a tank has.
    hitRadius (Number)
    * The radius, in metres, around the tank used to detect a projectile collision.
    collisionRadius (Number)
    * The radius, in metres, around the tank used to detect a collision with terrain objects.
    type (String)
    * Describes the type of tank (i.e. slow or fast).
    position (Array of Numbers)
    * The coordinates, in metres, of the tank on the map.
    tracks (Number)
    * The angle, in radians, of rotation of the tracks relative to the (1,0) unit vector.
    turret (Number)
    * The angle, in radians, of rotation of the turret relative to the (1,0) unit vector.
    speed (Number)
    * The maximum speed, in m/s, of the tank.
    projectiles (Projectile Array)
    * Describes attributes about all projectiles.
    """

    id = ""
    health = None
    hit_radius = None
    collision_radius = None
    type = ""
    position = []
    tracks = None
    turret = None
    speed = None
    projectiles = []

    def __init__(self, id, health, hit_radius, collision_radius, type, position, tracks, turret, speed, projectiles):
        self.id = id
        self.health = health
        self.hit_radius = hit_radius
        self.collision_radius = collision_radius
        self.type = type
        self.position = position
        self.tracks = tracks
        self.turret = turret
        self.speed = speed
        self.projectiles = projectiles

    def __eq__(self, other):
        basic_equality = self.id == other.id and self.health == other.health and self.hit_radius == other.hit_radius and \
                         self.collision_radius == other.collision_radius and self.type == other.type and \
                         self.position == other.position and self.tracks == other.tracks and self.turret == other.turret and \
                         self.speed == other.speed
        return basic_equality and str(sorted(self.projectiles)) == str(sorted(other.projectiles))

    def __str__(self):
        return "<Tank> %s; health %s; hit_radius %s; collision_radius %s; type %s; position %s; tracks %s; " \
               "turret %s; speed %s; projectiles %s" % (
                   self.id, self.health, self.hit_radius, self.collision_radius, self.type, str(self.position),
                   self.tracks, self.turret, self.speed, str(sorted(self.projectiles))
               )

    def __repr__(self):
        return "<Tank> %s; health %s; hit_radius %s; collision_radius %s; type %s; position %s; tracks %s; " \
               "turret %s; speed %s; projectiles %s" % (
                   self.id, self.health, self.hit_radius, self.collision_radius, self.type, str(self.position),
                   self.tracks, self.turret, self.speed, str(sorted(self.projectiles))
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

    def get_closest_tank(self, tanks):
        """
        Given the list of tanks as a parameter, return the closest enemy tank.
        :param tanks: List of tanks
        :return: Distance, Tank. None if no tanks.
        """
        min_dist = float('inf')
        closest_tank = None
        for tank in tanks:
            dist = math.hypot(tank.position[0] - self.position[0], tank.position[1] - self.position[1])
            if dist < min_dist:
                min_dist = dist
                closest_tank = tank
        return min_dist, closest_tank

    def get_rads_to_tank(self, tank):
        """
        Given the tank to point at, get the rads direction.
        Positive value means rotating counter clockwise, negative value means rotate clockwise
        :param tank: Tank to get rads to
        :return: Number (Float)
        """
        x = tank.position[0] - self.position[0]
        y = tank.position[1] - self.position[1]
        return math.atan2(y, x)

    def get_point_turret_to_tank(self, tank):
        """
        Given the tank to point the turret at, get the command for pointing this turret to that thank
        :param tank: Tank to point turret at
        """
        raw_rads = self.get_rads_to_tank(tank)
        oh_to_two_rads = (raw_rads + (2 * math.pi)) % (2 * math.pi)

        rotation = self.turret - oh_to_two_rads
        if rotation < 0:
            # rotation is CCW
            if abs(rotation) > math.pi:
                return 'CW', (2 * math.pi) - abs(rotation)
            else:
                return 'CCW', abs(rotation)
        else:
            # rotation is CW
            if abs(rotation) > math.pi:
                return 'CCW', (2 * math.pi) - rotation
            else:
                return 'CW', rotation

    def get_point_track_to_tank(self, tank):
        """
        Given the tank to point the turret at, get the command for pointing this track to that thank
        :param tank: Tank to point track at
        """
        raw_rads = self.get_rads_to_tank(tank)
        oh_to_two_rads = (raw_rads + (2 * math.pi)) % (2 * math.pi)

        rotation = self.tracks - oh_to_two_rads
        if rotation < 0:
            # rotation is CCW
            if abs(rotation) > math.pi:
                return 'CW', (2 * math.pi) - abs(rotation)
            else:
                return 'CCW', abs(rotation)
        else:
            # rotation is CW
            if abs(rotation) > math.pi:
                return 'CCW', (2 * math.pi) - rotation
            else:
                return 'CW', rotation
    def get_dist_to_tank(self, tank):
        """
        Return the distance from the tank to the specified point.
        :param tank: tank object containing position 2-tuple
        :return: float, value of distance
        """
        return math.hypot(tank.position[0] - self.position[0], tank.position[1] - self.position[1])

    def is_friendly_fire(self, tanks, enemy_dist, enemy_tank):
        """
        Given the ally tanks and the enemy tank our current tank wants to shoot. Check that no allies are in the way
        and return True if it is a safe shot.
        :param tanks: Ally tanks
        :param enemy_dist: Distance to enemy tank
        :param enemy_tank: Enemy tank that current tank is trying to shoot
        :return boolean
        """

        EPSILON = 1e-6
        # http://math.stackexchange.com/questions/275529/check-if-line-intersects-with-circles-perimeter
        a = enemy_tank.position[0] - self.position[0]
        b = self.position[1] - enemy_tank.position[1]
        c = a * self.position[1] + self.position[0] * b
        for tank in tanks:
            if self.id == tank.id:
                continue  # cannot shoot self
            rs = self.get_rads_to_tank(tank)
            # check if shooting at enemy_tank hits any allies hit circles
            # if it does hit an ally, check that the enemy is closer than the ally
            ally_radius = tank.collision_radius
            # draw a line from current tank to enemy, and check if the ally is in the way
            if ((math.fabs(a * tank.position[0] + b * tank.position[1] + c) / math.sqrt(a * a + b * b)) <= (
                            2 * ally_radius + EPSILON)):
                dist = math.hypot(tank.position[0] - self.position[0], tank.position[1] - self.position[1])
                if enemy_dist - EPSILON > dist:  # ally between current tank and enemy
                    return True
        return False