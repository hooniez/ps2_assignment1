from enum import Enum

class Direction(Enum):
    NORTH = "north"
    NORTH_EAST = "north east"
    EAST = "east"
    SOUTH_EAST = "south east"
    SOUTH = "south"
    SOUTH_WEST = "south west"
    WEST = "west"
    NORTH_WEST = "north west"

    @classmethod
    def getDirection(cls, vector):
        if vector.x > -0.33 and vector.x < 0.33 and vector.z < -0.66:
            return cls.NORTH
        elif vector.z > -0.66 and vector.z < -0.33 and vector.x > 0.33:
            return cls.NORTH_EAST
        elif vector.z > -0.33 and vector.z < 0.33 and vector.x > 0.66:
            return cls.EAST
        elif vector.x < 0.66 and vector.x > 0.33 and vector.z > 0.33:
            return cls.SOUTH_EAST
        elif vector.x < 0.33 and vector.x > -0.33 and vector.z > 0.66:
            return cls.SOUTH
        elif vector.z < 0.66 and vector.z > 0.33 and vector.x < -0.33:
            return cls.SOUTH_WEST
        elif vector.z < 0.33 and vector.z > -0.33 and vector.x > 0.66:
            return cls.WEST
        elif vector.x > -0.66 and vector.x < -0.33 and vector.z < 0.66:
            return cls.NORTH_WEST


    @classmethod
    def getCardinalDirection(cls, vector):
        if abs(vector.x) > abs(vector.z) and vector.x < 0: #facing west
            return cls.WEST
        elif abs(vector.x) > abs(vector.z) and vector.x > 0: #facing east
            return cls.EAST
        elif abs(vector.x) < abs(vector.z) and vector.z < 0: #facing north
            return cls.NORTH
        elif abs(vector.x) < abs(vector.z) and vector.z > 0: #facing south
            return cls.SOUTH