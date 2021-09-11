import random
import math
import datetime
import mcpi.block as block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from foundation import Foundation


SPAWN_DISTANCE_FROM_PLAYER = 10

def get_height_actual_block(x, z):
    ''' Ensure blocks like LEAVES are excluded from the method mc.getHeight'''
    blocks_to_avoid = [block.LEAVES.id]
    height = mc.getHeight(x,z)
    random_block = mc.getBlock(x, height, z)
    while random_block in blocks_to_avoid:
        height -= 1
        random_block = mc.getBlock(x, height, z)
    return height


class Village():
    def __init__(self, playerPos, playerDirection, foundationSize=10, villageAreaSize=100, numHouses=8):
        self.foundations = []
        self.villageAreaSize = villageAreaSize
        self.foundationSize = foundationSize
        self.numHouses = numHouses
        #set the bounding box based on the direction the player is facing
        if abs(playerDirection.x) > abs(playerDirection.z) and playerDirection.x < 0: #facing west
            print("the player is facing west")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x - SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z - (villageAreaSize // 2)),
                "southEast": Vec3(playerPos.x - SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "southWest": Vec3(playerPos.x - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "northWest": Vec3(playerPos.x - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z - (villageAreaSize // 2))
            }
        elif abs(playerDirection.x) > abs(playerDirection.z) and playerDirection.x > 0: #facing east
            print("the player is facing east")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x + SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z - (villageAreaSize // 2)),
                "southEast": Vec3(playerPos.x + SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "southWest": Vec3(playerPos.x + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "northWest": Vec3(playerPos.x + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z - (villageAreaSize // 2))
            }
        elif abs(playerDirection.x) < abs(playerDirection.z) and playerDirection.z < 0: #facing north
            print("the player is facing north")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER)),
                "southEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z - SPAWN_DISTANCE_FROM_PLAYER),
                "southWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z - SPAWN_DISTANCE_FROM_PLAYER),
                "northWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER))
            }
        elif abs(playerDirection.x) < abs(playerDirection.z) and playerDirection.z > 0: #facing south
            print("the player is facing south")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER)),
                "southEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z + SPAWN_DISTANCE_FROM_PLAYER),
                "southWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z + SPAWN_DISTANCE_FROM_PLAYER),
                "northWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER))
            }
        print(self.boundingBox)
    
    
    #for testing only - to fill the full village area
    def displayBoundingBox(self):
        mc.setBlocks(
            self.boundingBox["northWest"].x,
            self.boundingBox["northWest"].y,
            self.boundingBox["northWest"].z,
            self.boundingBox["southEast"].x,
            self.boundingBox["southEast"].y,
            self.boundingBox["southEast"].z,
            block.BOOKSHELF.id
        )

    #find the center of the group of foundations (not currently used, but will later for instersections)
    def findCentroid(self, centerPoints):
        length = len(centerPoints)

        if length < 1:
            return Vec3(0,0,0)
        elif length == 1:
            return centerPoints[0]

        centroid = Vec3(sum([p.x for p in centerPoints]) / length, sum([p.y for p in centerPoints]) / length, sum([p.z for p in centerPoints]) / length)
        return centroid
    
    def _getDistance(self, p1, p2):
        return math.sqrt(((p2.x - p1.x)**2) + ((p2.y - p1.y)**2) + ((p2.z - p1.z)**2))

    # connects each foundation to it's closest neighbour that remains in the unconnected list
    # currently only connects one other foundation, but will expand to more + intersections
    def groupProximalFoundations(self, foundations):
        remaining = [f for f in foundations]

        for point in foundations:
            if len(remaining) <= 1:
                break

            minDist = min([self._getDistance(r.center_vector, point.center_vector) for r in remaining if r != point])
            closestFoundation = [r for r in remaining if self._getDistance(r.center_vector, point.center_vector) == minDist][0]
            print(f"closest to {point.center_vector}: {closestFoundation.center_vector}")
            point.neighbour = closestFoundation
            closestFoundation.neighbour = point

    def layFoundations(self):
        count = 1
        for foundation in self.foundations:
            foundation.placeFoundation(mc)
            mc.setBlock(
                foundation.boundingBox["centerPoint"].x,
                foundation.boundingBox["centerPoint"].y,
                foundation.boundingBox["centerPoint"].z,
                block.WOOL.id,
                count
            )
            count += 1

    def generateFoundations(self):
        xVals = None
        zVals = None
        ZRange = None
        minDist = self.foundationSize + 2
        print(self.foundationSize)
        print(minDist)
        
        if self.boundingBox["northWest"].x < self.boundingBox["northEast"].x:
            xVals = sorted(random.sample(range(self.boundingBox["northWest"].x, self.boundingBox["northEast"].x), self.numHouses))
        else:
            xVals = sorted(random.sample(range(self.boundingBox["northEast"].x, self.boundingBox["northWest"].x), self.numHouses))
        
        if self.boundingBox["southEast"].z < self.boundingBox["northEast"].z:
            ZRange = [n for n in range(self.boundingBox["southEast"].z, self.boundingBox["northEast"].z)]
            zVals = random.sample(ZRange, self.numHouses)
        else:
            ZRange = range(self.boundingBox["northEast"].z, self.boundingBox["southEast"].z)
            zVals = random.sample(ZRange, self.numHouses)

        # if every second foundation is too close, move it to the minimum distance based on the foundation size
        # foundations with adjacent x vals are dealt with later
        for i in range(2, len(xVals) - 1):
            xDiff = (xVals[i] - xVals[i - 2])
            print(f"center point distance from {xVals[i]} to {xVals[i - 2]}: {xDiff}")
            if xDiff < minDist:
                xVals[i] += minDist - xDiff


        print(xVals)
        print(zVals)
        
        previousVals = None
        for x, z in zip(xVals, zVals):
            # if the foundations are too close together, pick a new z val that isn't already taken
            if previousVals is not None and (x - previousVals[0]) < minDist and (z - previousVals[1]) < minDist:
                print(f"old z: {z}")
                print(range(previousVals[1] - minDist, previousVals[1] + minDist))
                possibleZVals = [n for n in ZRange if n not in range(previousVals[1] - minDist, previousVals[1] + minDist)]
                z = random.choice(possibleZVals)
                print(f"new z: {z}")

            self.foundations.append(Foundation(Vec3(x, 0, z), self.foundationSize))

            previousVals = (x, z)


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    mc = Minecraft.create()
    print(mc.player.getDirection())
    village = Village(mc.player.getTilePos(), mc.player.getDirection(), 25, 200, 9)
    # village.displayBoundingBox()
    village.generateFoundations()
    village.layFoundations()
    endTime = datetime.datetime.now()

    time_diff = (endTime - startTime)
    execution_time = time_diff.total_seconds()
    print(f"runtime: {execution_time}")
