import random
import math
import datetime
from path import Path as path
from direction import Direction
import mcpi.block as block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from foundation import Foundation
from house import house

SPAWN_DISTANCE_FROM_PLAYER = 10



class Village():
    def __init__(self, playerPos, playerDirection, foundationSize=10, villageAreaSize=100, numHouses=8):
        self.foundations = []
        self.houses = []
        self.paths = []
        self.villageAreaSize = villageAreaSize
        self.foundationSize = foundationSize
        self.numHouses = numHouses
        #set the bounding box based on the direction the player is facing
        if Direction.getCardinalDirection(playerDirection) == Direction.WEST:
            print("the player is facing west")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x - SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z - (villageAreaSize // 2)),
                "southEast": Vec3(playerPos.x - SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "southWest": Vec3(playerPos.x - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "northWest": Vec3(playerPos.x - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z - (villageAreaSize // 2))
            }
        elif Direction.getCardinalDirection(playerDirection) == Direction.EAST:
            print("the player is facing east")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x + SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z - (villageAreaSize // 2)),
                "southEast": Vec3(playerPos.x + SPAWN_DISTANCE_FROM_PLAYER, playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "southWest": Vec3(playerPos.x + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z + (villageAreaSize // 2)),
                "northWest": Vec3(playerPos.x + (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER), playerPos.y, playerPos.z - (villageAreaSize // 2))
            }
        elif Direction.getCardinalDirection(playerDirection) == Direction.NORTH:
            print("the player is facing north")
            self.boundingBox = {
                "northEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER)),
                "southEast": Vec3(playerPos.x - (villageAreaSize // 2), playerPos.y, playerPos.z - SPAWN_DISTANCE_FROM_PLAYER),
                "southWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z - SPAWN_DISTANCE_FROM_PLAYER),
                "northWest": Vec3(playerPos.x + (villageAreaSize // 2), playerPos.y, playerPos.z - (villageAreaSize + SPAWN_DISTANCE_FROM_PLAYER))
            }
        elif Direction.getCardinalDirection(playerDirection) == Direction.SOUTH:
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

    #find the center of the group of foundations (not currently used, but will later for path instersections)
    def findCentroid(self, centerPoints):
        length = len(centerPoints)

        if length < 1:
            return Vec3(0,0,0)
        elif length == 1:
            return centerPoints[0]

        centroid = Vec3(
            sum([p.x for p in centerPoints]) / length,
            sum([p.y for p in centerPoints]) / length,
            sum([p.z for p in centerPoints]) / length
        )
        return centroid


    # connects each foundation to it's closest neighbours that remains in the unconnected list
    def groupProximalFoundations(self):
        remaining = [f for f in self.foundations]

        for point in self.foundations:
            if len(remaining) <= 1:
                break

            minDist = min([point.getDistance(r) for r in remaining if r != point])
            closestFoundation = [r for r in remaining if point.getDistance(r) == minDist][0]
            point.neighbours.append(closestFoundation)
            if point not in closestFoundation.neighbours:
                closestFoundation.neighbours.append(point)

            remaining.remove(point)


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
        minDist = self.foundationSize + 22
        
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
            if xDiff < minDist:
                xVals[i] += minDist - xDiff

        previousVals = None
        count = 1
        for x, z in zip(xVals, zVals):
            # if the foundations are too close together, pick a new z val that isn't already taken
            if previousVals is not None and (x - previousVals[0]) < minDist and (z - previousVals[1]) < minDist:
                possibleZVals = [n for n in ZRange if n not in range(previousVals[1] - minDist, previousVals[1] + minDist)]
                z = random.choice(possibleZVals)

            self.foundations.append(Foundation(mc, Vec3(x, 0, z), self.foundationSize, count))
            count += 1
            previousVals = (x, z)

    def generateHouses(self):
        for foundation in self.foundations:
            foundation.setBase(mc)
            house_ = house(foundation)
            self.houses.append(house_)

            #Zain create a for loop that randomises the amount of floors generated. 

            print('Create Floor 0')
            house_.createFloor()
            house_.floors[0].addRoom(mc)
            house_.floors[0].addRoom(mc)
            house_.floors[0].addRoom(mc)
            house_.floors[0].addRoom(mc)
            house_.floors[0].addRoom(mc)
            house_.floors[0].addDoors(mc)

            print('Create Floor 1')
            house_.createFloor()
            house_.floors[1].addRoom(mc)
            house_.floors[1].addRoom(mc)
            house_.floors[1].addRoom(mc)
            house_.floors[1].addDoors(mc)
            
            print('Create Floor 2')
            house_.createFloor()
            house_.floors[2].addRoom(mc)
            house_.floors[2].addRoom(mc)
            house_.floors[2].addDoors(mc)


            #These functions are added at the end as their scope is the entire house / must be done after all rooms have been created
            
            # Best to use this order, changing the order of calls may effect the workings of the functions
            print('Implement global hourse styles')
            house_.floors[0].addFrontDoor(mc)
            house_.addAllStairs(mc)
            hourse_.addAllWindows(mc)
            house_.addAllRoofs(mc)

            
            
            



if __name__ == '__main__':
    startTime = datetime.datetime.now()
    mc = Minecraft.create()
    village = Village(mc.player.getTilePos(), mc.player.getDirection(), 25, 200, 9)
    # village.displayBoundingBox()
    village.generateFoundations()
    village.layFoundations()
    village.generateHouses()
    village.groupProximalFoundations()
    for foundation in village.foundations:
        print(f"foundation {foundation.id}:")
        for neighbour in foundation.neighbours:
            print(f"    - to foundation {neighbour.id}:")
            if (foundation.id, neighbour.id) not in village.paths:
                print(f"        -- path point start at {foundation.getPathPoint(foundation.getDirection(neighbour))}")
                path.generatePath(
                    foundation.getPathPoint(foundation.getDirection(neighbour)),
                    neighbour.getPathPoint(neighbour.getDirection(foundation)),
                    foundation.getDirection(neighbour),
                    mc
                )
                village.paths.append((foundation.id, neighbour.id))
                village.paths.append((neighbour.id, foundation.id))
            else:
                print("         -- path already exists")

    endTime = datetime.datetime.now()

    for foundation in village.foundations:
        print(f"foundation {foundation.id} - closest: {[f.id for f in foundation.neighbours]}")

    time_diff = (endTime - startTime)
    execution_time = time_diff.total_seconds()
    print(f"runtime: {execution_time}")
