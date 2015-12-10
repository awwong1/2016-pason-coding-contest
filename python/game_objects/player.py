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
