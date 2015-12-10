from command import Command


class Obstacle:
    """
    Bounding box obstacle.
    obs_type (String)
    * Describes the type of terrain object it is (i.e SOLID or IMPASSABLE).
    corner (Integer Array)
    * The coordinates, in metres, of the corner of the terrain closest to the map origin.
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


class Map:
    """
    Map origin (0, 0) is bottom left
    size (Integer Tuple)
    * The width and height, in metres, of the game map (In that order).
    obstacles (Obstacle Array)
    * Array of obstacles on the map
    """
    size = []
    obstacles = []

    def __init__(self, size, obstacles):
        self.size = size
        self.obstacles = obstacles

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


class Player:
    """
    players structure
    score (Integer)
    * The current score for the team.
    name (String)
    * The name of the team.
    tanks (Tank Array)
    * Describes attributes about the tanks belonging to a team.
    """
    score = None
    name = ""
    tanks = []

    def __init__(self, name, score, tanks):
        self.name = name
        self.score = score
        self.tanks = tanks

    def __eq__(self, other):
        basic_equality = self.score == other.score and self.name == other.name
        return basic_equality and str(sorted(self.tanks)) == str(sorted(other.tanks))

    def __str__(self):
        return "<Player> %s; score %s; %s" % (self.name, self.score, str(self.tanks))

    def __repr__(self):
        return "<Player> %s; score %s; %s" % (self.name, self.score, str(self.tanks))

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


class Algorithm:
    """
    Calculates the actions for the current game state.

    json_game_state structure
    comm_type
    * String
    * The message type to indicate that this is a game state message.
    timeRemaining
    * Number
    * The amount of time, in seconds, remaining in the game.
    timestamp
    * Number
    * The current time, in milliseconds, that this state was generated.

    map
    * Object
    * Describes the various attributes about the game map.

    players
    * Array of Objects
    * Describes various attributes about the players in the game.
    """
    team_name = ""
    time_remaining = ""
    map = None
    players = []

    def __init__(self, team_name):
        self.team_name = team_name

    def parse_game_state(self, json_game_state):
        self.time_remaining = json_game_state['timeRemaining']
        map_size = json_game_state['map']['size'][0], json_game_state['map']['size'][1]
        map_obstacles = []
        for terrain in json_game_state['map']['terrain']:
            map_obstacles.append(
                Obstacle(terrain['type'], terrain['boundingBox']['corner'], terrain['boundingBox']['size'])
            )
        self.map = Map(map_size, map_obstacles)

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
                    Tank(id, health, hit_radius, collision_radius, type, position, tracks, turret, speed, projectiles))
            self.players.append(Player(name, score, tanks))

        return []
