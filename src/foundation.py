import math
from direction import Direction
from mcpi.vec3 import Vec3
import mcpi.block as block

class Foundation():
    def __init__(self, centerPoint, size, fId):
        self.id = fId
        self.boundingBox = {
                "northEast": Vec3(centerPoint.x + (size // 2), centerPoint.y, centerPoint.z - (size // 2)),
                "southEast": Vec3(centerPoint.x + (size // 2), centerPoint.y, centerPoint.z + (size // 2)),
                "southWest": Vec3(centerPoint.x - (size // 2), centerPoint.y, centerPoint.z + (size // 2)),
                "northWest": Vec3(centerPoint.x - (size // 2), centerPoint.y, centerPoint.z - (size // 2)),
               "centerPoint": centerPoint
            }
        self.neighbours = []

    #calculates length of the vector from self to compare
    def getDistance(self, compare):
        return math.sqrt(
            ((compare.boundingBox["centerPoint"].x - self.boundingBox["centerPoint"].x)**2)
            + ((compare.boundingBox["centerPoint"].y - self.boundingBox["centerPoint"].y)**2)
            + ((compare.boundingBox["centerPoint"].z - self.boundingBox["centerPoint"].z)**2)
        )

    #calculates the directional unit vector from self to compare, then returns the appropriate cardinal direction enum
    def getDirection(self, compare):
        magnitude = self.getDistance(compare)
        unitVector = Vec3(
            (compare.boundingBox["centerPoint"].x - self.boundingBox["centerPoint"].x) / magnitude,
            (compare.boundingBox["centerPoint"].y - self.boundingBox["centerPoint"].y) / magnitude,
            (compare.boundingBox["centerPoint"].z - self.boundingBox["centerPoint"].z) / magnitude
        )
        return Direction.getCardinalDirection(unitVector)


    def getPathPoint(self, direction):
        if direction == Direction.NORTH:
            return Vec3(
                self.boundingBox["northEast"].x - ((self.boundingBox["northEast"].x - self.boundingBox["northWest"].x) // 2),
                self.boundingBox["northEast"].y,
                self.boundingBox["northEast"].z
            )
        elif direction == Direction.EAST:
            return Vec3(
                self.boundingBox["northEast"].x,
                self.boundingBox["northEast"].y,
                self.boundingBox["southEast"].z - ((self.boundingBox["southEast"].z - self.boundingBox["northEast"].z) // 2)
            )
        elif direction == Direction.SOUTH:
            return Vec3(
                self.boundingBox["southEast"].x - ((self.boundingBox["southEast"].x - self.boundingBox["southWest"].x) // 2),
                self.boundingBox["southEast"].y,
                self.boundingBox["southEast"].z
            )
        elif direction == Direction.WEST:
            return Vec3(
                self.boundingBox["northWest"].x,
                self.boundingBox["northWest"].y,
                self.boundingBox["southWest"].z - ((self.boundingBox["southWest"].z - self.boundingBox["northWest"].z) // 2)
            )

    def _addFoundationSupports(self, mc):
        for (key, item) in self.boundingBox.items():
            if key != "centerPoint":
                mc.setBlocks(
                    item.x,
                    item.y - 1,
                    item.z,
                    item.x,
                    item.y - 150,
                    item.z,
                    block.BEDROCK.id
                )

    def _clearFoundationSpace(self, mc):
        mc.setBlocks(
            self.boundingBox["northEast"].x,
            self.boundingBox["northEast"].y + 1,
            self.boundingBox["northEast"].z,
            self.boundingBox["southWest"].x,
            self.boundingBox["southWest"].y + 41,
            self.boundingBox["southWest"].z,
            block.AIR.id
        )


    def _adjustYToEnvironment(self, mc):
        invalidBlocks = [block.WOOD.id, block.LEAVES.id, block.LEAVES2.id]

        envHeights = [mc.getHeight(p.x, p.z) for p in self.boundingBox.values() if mc.getBlock(p.x, mc.getHeight(p.x, p.z), p.z) not in invalidBlocks]
        highestPoint = max(envHeights) if len(envHeights) > 0 else mc.getHeight(self.boundingBox["centerPoint"].x, self.boundingBox["centerPoint"].z)

        for point in self.boundingBox.values():
            point.y = highestPoint


    def placeFoundation(self, mc):
        self._adjustYToEnvironment(mc)
        mc.setBlocks(
            self.boundingBox["northEast"].x,
            self.boundingBox["northEast"].y,
            self.boundingBox["northEast"].z,
            self.boundingBox["southWest"].x,
            self.boundingBox["southWest"].y,
            self.boundingBox["southWest"].z,
            block.BEDROCK.id
        )
        print(f'foundation placed at: {self.boundingBox["centerPoint"].x}, {self.boundingBox["centerPoint"].y}, {self.boundingBox["centerPoint"].z}')
        self._clearFoundationSpace(mc)
        self._addFoundationSupports(mc)

