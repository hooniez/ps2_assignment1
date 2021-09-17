import math
import mcpi.block as block
from mcpi.vec3 import Vec3
from direction import Direction
from numpy import linspace
from pathPoint import PathPoint

class Path:
    # the longest distance will be the one that covers the y height changes

    @classmethod
    def _balanceStairNumbers(cls, distX, distY, distZ):
        stairsNeeded = math.ceil(abs(distZ) / 3)
        maxXStairs = (abs(distX) // 3) - 1 if (abs(distX) // 3) - 1 >= 0 else 0
        maxZStairs = (abs(distZ) // 3) - 1 if (abs(distZ) // 3) - 1 >= 0 else 0
        ZStairs = stairsNeeded // 2
        XStairs = math.ceil(stairsNeeded / 2)
        print(f"        -- stairs needed = {stairsNeeded}")
        print(f"        -- max X stairs: {maxXStairs} max Z stairs: {maxZStairs}")
        print(f"        -- in function xStairs: {XStairs} & zStairs: {ZStairs}")
        #check if the z dist can be covered
        if ((XStairs > maxXStairs and ZStairs + (XStairs - maxXStairs) > maxZStairs) or
                (ZStairs > maxZStairs and XStairs + (ZStairs - maxZStairs) > maxXStairs)):
            print("****can't cover y dist****")
            #do something else to solve
            return (0, 0)

        if XStairs > maxXStairs:
            ZStairs += XStairs - maxXStairs
            XStairs -= XStairs - maxXStairs

        if ZStairs > maxZStairs:
            XStairs += ZStairs - maxZStairs
            ZStairs -= ZStairs - maxZStairs

        return (XStairs, ZStairs)


    @classmethod
    def generatePath(cls, start, end, startDirection, mc):
        distX = end.x - start.x
        distY = end.y - start.y
        distZ = end.z - start.z
        xStairs, zStairs = cls._balanceStairNumbers(distX, distY, distZ)
        
        print(f"        -- xStairs: {xStairs} & zStairs: {zStairs}")
        if zStairs < 0 or xStairs < 0:
            print("****negative number of stairs****")
            return
        
        currPos = start
        if startDirection == Direction.EAST or startDirection == Direction.WEST:
            split1 = xStairs // 2 if xStairs % 2 == 0 else (xStairs // 2) + 1
            split2 = xStairs // 2
            currPos = cls.pathLayer(currPos, Vec3(currPos.x + (distX // 2), end.y, currPos.z), split1, 0, mc) # go east or west
            currPos = cls.pathLayer(currPos, Vec3(currPos.x, end.y, end.z), 0, zStairs, mc) # go north or south
            currPos = cls.pathLayer(currPos, end, split2, 0, mc)
        else:
            split1 = zStairs // 2 if zStairs % 2 == 0 else (zStairs // 2) + 1
            split2 = zStairs // 2
            currPos = cls.pathLayer(currPos, Vec3(currPos.x, end.y, currPos.z + (distZ // 2)), 0, split1, mc) # go north or south
            currPos = cls.pathLayer(currPos, Vec3(end.x, end.y, currPos.z), xStairs, 0, mc) # go east or west
            currPos = cls.pathLayer(currPos, end, 0, split2, mc) 

    #create list of tuples that contain the start and end vectors for each section of the  path
    @classmethod
    def routePlanner(cls):
        route = []
        


    #not working properly - may need to change approach to planning the exact coords in a list
    # and then feed the list to the  builder to make it easier to debug
    @classmethod
    def pathLayer(cls, start, end, xStairs, zStairs, mc):
        stepX = (end.x - start.x) // abs(end.x - start.x) if end.x - start.x != 0 else 0
        stepY = (end.y - start.y) // abs(end.y - start.y) if end.y - start.y != 0 else 0
        stepZ = (end.z - start.z) // abs(end.z - start.z) if end.z - start.z != 0 else 0
        workingRangeX = range(start.x, end.x) if start.x <= end.x else range(end.x, start.x)
        workingRangeZ = range(start.z, end.z) if start.z <= end.z else range(end.z, start.z)

        xStairSpacing = (
            [math.floor(n) for n in linspace(start.x + 2, end.x - 4, xStairs)] if end.x > start.x 
                else [math.floor(n) for n in linspace(end.x + 2, start.x - 4, xStairs)]
        )

        zStairSpacing = (
            [math.floor(n) for n in linspace(start.z + 2, end.z - 3, zStairs)] if end.z > start.z 
                else [math.floor(n) for n in linspace(end.z + 2, start.z - 3, zStairs)]
        )

        currPos = start
        for point in xStairSpacing:
            targetPos = Vec3(point, currPos.y, currPos.z)
            currPos = cls._layFlatPath(currPos, targetPos, block.COBBLESTONE, mc)

            if abs(end.y - currPos.y) > 3 :
                targetPos = Vec3(currPos.x + (3 * stepX), currPos.y + (3 * stepY), currPos.z)
            else:
                targetPos = Vec3(currPos.x + (abs(end.y - start.y) * stepX), currPos.y + (abs(end.y - start.y) * stepY), currPos.z)

            currPos = cls._layStairCase(currPos, targetPos, block.COBBLESTONE, mc)
            xStairSpacing.remove(point)
            if currPos.x not in workingRangeX:
                break


        for point in zStairSpacing:
            targetPos = Vec3(currPos.x, currPos.y, point)
            currPos = cls._layFlatPath(currPos, targetPos, block.COBBLESTONE, mc)
            
            if abs(end.y - currPos.y) > 3 :
                targetPos = Vec3(currPos.x, currPos.y + (3 * stepY), currPos.z + (3 * stepZ))
            else:
                targetPos = Vec3(currPos.x, currPos.y + (abs(end.y - start.y) * stepY), currPos.z + (abs(end.y - start.y) * stepZ))

            currPos = cls._layStairCase(currPos, targetPos, block.COBBLESTONE, mc)
            zStairSpacing.remove(point)
            if currPos.z not in workingRangeZ:
                break
        
        return cls._layFlatPath(currPos, end, block.COBBLESTONE, mc)


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
        for i in range(abs(start.y - end.y)):
            print(f" step {i}: {currPos}")
            currPos = Vec3(
                start.x + (i * stepX),
                start.y + (i * stepY),
                start.z + (i * stepZ)
            )
            mc.setBlock(currPos.x, currPos.y, currPos.z, blockType.id)

        return currPos



# class intersection:



if __name__ == '__main__':
    pass
