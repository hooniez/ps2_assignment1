import math
import mcpi.block as block
from mcpi.vec3 import Vec3

class Walkway:
    def __init__(self, start: Vec3, end: Vec3, connection):
        self.pathBlockType = block.STONE
        self.pathRailType = block.FENCE
        self.start = start
        self.end = end
        self.distX = end.x - start.x
        self.distY = end.y - start.y
        self.distZ = end.z - start.z
        self.staircasesNeeded = math.ceil(self.distZ / 3)
        self.currPos = start
        self.currTarget = None
        self.mc = connection


    #note to self --- currpos will need rethinking when expanding as it's not sure what it wants to be
    #it's currently between 2 ways of acheiving the goal, but not satisfying either
    #distX etc will need to be dynamic

    def generatePath(self):
        #if statement checks will determine the starting side of the foundation for the path
        # east/west check
        if self.distX < 0: # go west
            self.currTarget = Vec3(self.start.x + self.distX, self.start.y, self.start.z)
            self._layFlatPath(self.start, self.currTarget)
        elif self.distX > 0: # go east
            self.currTarget = Vec3(self.start.x + self.distX, self.start.y, self.start.z)
            self._layFlatPath(self.start, self.currTarget)
        # else stay on same x coord
        
        # north/south check
        if self.distZ < 0: # go north
            self.currTarget = self.end
            self._layFlatPath(self.currentPos, self.currTarget)
        elif self.distZ > 0: # go south
            self.currTarget = self.end
            self._layFlatPath(self.currentPos, self.currTarget)
        # else stay on same Z coord

        print(f"path to {self.currentPos} completed")
        print()



    def _layFlatPath(self, start, end):
        self.mc.setBlocks(start.x, start.y, start.z, end.x, end.y, end.z, self.pathBlockType.id)
        self.currentPos = end
    
    def _layStairCase(self):
        pass


# class intersection:



if __name__ == '__main__':
    pass
