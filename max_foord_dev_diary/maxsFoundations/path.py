import mcpi.block as block
from mcpi.vec3 import Vec3
from pathPoint import PathPoint
from routePlan import RoutePlan

class Path:

    @classmethod
    def generatePath(cls, startFoundation, endFoundation, mc):
        start = startFoundation.getPathPoint(endFoundation)
        end = endFoundation.getPathPoint(startFoundation)
        startDirection = startFoundation.getDirection(endFoundation)

        route = RoutePlan(start, end, startDirection)
        route.planRoute()

        print(route)

        cls._pathLayer(route, mc)

    #not working properly - may need to change approach to planning the exact coords in a list
    # and then feed the list to the  builder to make it easier to debug
    @classmethod
    def _pathLayer(cls, route, mc):
        for leg in route.getLegs():
            for point in leg:
                if point.start.y == point.end.y:
                    cls._layFlatPath(point.start, point.end, block.COBBLESTONE, mc)
                else:
                    cls._layStairCase(point.start, point.end, block.COBBLESTONE, mc)



    @classmethod
    def _layFlatPath(cls, start, end, blockType, mc):
        mc.setBlocks(start.x, start.y, start.z, end.x, end.y, end.z, blockType.id)
        return end
    

    @classmethod
    def _layStairCase(cls, start, end, blockType, mc):
        stepX = (end.x - start.x) // abs(end.x - start.x) if end.x - start.x != 0 else 0
        stepY = (end.y - start.y) // abs(end.y - start.y) if end.y - start.y != 0 else 0
        stepZ = (end.z - start.z) // abs(end.z - start.z) if end.z - start.z != 0 else 0
        currPos = start
        print(f"{Vec3(stepX, stepY, stepZ)}")

        for i in range(1, abs(start.y - end.y) + 1):
            print(f" step {i}: {currPos}")
            currPos = Vec3(
                start.x + (i * stepX),
                start.y + (i * stepY),
                start.z + (i * stepZ)
            )
            mc.setBlock(currPos.x, currPos.y, currPos.z, blockType.id)

        return currPos


if __name__ == '__main__':
    pass
