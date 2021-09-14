import math
import mcpi.block as block
from mcpi.vec3 import Vec3
from direction import Direction

class Path:
    # the longest distance will be the one that covers the y height changes

    def generatePath(self, start, end, startDirection, mc):
        distX = end.x - start.x
        distY = end.y - start.y
        distZ = end.z - start.z
        staircasesNeeded = math.ceil(distZ / 3)
        currTarget = None
        currPos = start
        
        
        if (startDirection == Direction.EAST or startDirection == Direction.WEST):
            currTarget = Vec3(currPos.x + distX // 2, currPos.y, currPos.z)
            currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)

            currTarget = Vec3(currPos.x, currPos.y, currPos.z + distZ)
            currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)
        else:
            currTarget = Vec3(currPos.x, currPos.y, currPos.z + distZ // 2)
            currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)
            
            currTarget = Vec3(currPos.x + distX, currPos.y, currPos.z)
            currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)
        
        currTarget = Vec3(currPos.x, end.y, currPos.z)
        currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)

        currTarget = Vec3(end.x, end.y, end.z)
        currPos = self._layFlatPath(currPos, currTarget, block.COBBLESTONE, mc)


    def _layFlatPath(self, start, end, blockType, mc):
        mc.setBlocks(start.x, start.y, start.z, end.x, end.y, end.z, blockType.id)
        return end
    
    def _layStairCase():
        pass


# class intersection:



if __name__ == '__main__':
    pass
