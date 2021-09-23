import math
from mcpi.vec3 import Vec3
from pathPoint import PathPoint
from direction import Direction
from numpy import linspace


class RoutePlan:

    def  __init__(self, start, end, direction):
        self.start = start
        self.end = end
        #come back to this - potentially unnessesary calc now that distance is included?
        self.distance = Vec3(end.x - start.x, end.y - start.y, end.z - start.z)
        self.stepX = (end.x - start.x) // abs(end.x - start.x) if end.x - start.x != 0 else 0
        self.stepY = (end.y - start.y) // abs(end.y - start.y) if end.y - start.y != 0 else 0
        self.stepZ = (end.z - start.z) // abs(end.z - start.z) if end.z - start.z != 0 else 0
        self.direction = direction
        self.leg1 = None
        self.leg2 = None
        self.leg3 = None
        self.xStairs = 0
        self.zStairs = 0


    def __str__(self):
        return f"        -- Route: {{\n        --     Leg 1: {[p.__str__() for p in self.leg1]},\n        --     Leg 2: {[p.__str__() for p in self.leg2]},\n        --     Leg 3: {[p.__str__() for p in self.leg3]},\n        -- }}"


    def getLegs(self):
        return [self.leg1, self.leg2, self.leg3]


    def _balanceStairNumbers(self):
        stairsNeeded = math.ceil(abs(self.distance.y) / 3)
        maxXStairs = (abs(self.distance.x) // 3) - 1 if (abs(self.distance.x) // 3) - 1 >= 0 else 0
        maxZStairs = (abs(self.distance.z) // 3) - 1 if (abs(self.distance.z) // 3) - 1 >= 0 else 0
        self.zStairs = stairsNeeded // 2
        self.xStairs = math.ceil(stairsNeeded / 2)
        print(f"        -- stairs needed = {stairsNeeded}")
        print(f"        -- max X stairs: {maxXStairs} max Z stairs: {maxZStairs}")
        print(f"        -- in function xStairs: {self.xStairs} & zStairs: {self.zStairs}")
        #check if the z dist can be covered
        if ((self.xStairs > maxXStairs and self.zStairs + (self.xStairs - maxXStairs) > maxZStairs) or
                (self.zStairs > maxZStairs and self.xStairs + (self.zStairs - maxZStairs) > maxXStairs)):
            print("        -- ****can't cover y dist****")
            #do something else to solve
            return

        if self.xStairs > maxXStairs:
            self.zStairs += self.xStairs - maxXStairs
            self.xStairs -= self.xStairs - maxXStairs

        if self.zStairs > maxZStairs:
            self.xStairs += self.zStairs - maxZStairs
            self.zStairs -= self.zStairs - maxZStairs

        print(f"        -- xStairs: {self.xStairs} & zStairs: {self.zStairs}")
        if self.zStairs < 0 or self.xStairs < 0:
            print("****negative number of stairs****")


    def _spaceValues(self, num1, num2, numVals):
        print(f"        -- num1: {num1}, num2:{num2}, numVals: {numVals}")
        if num1 < num2:
            return sorted([math.floor(n) for n in linspace(num1 + 3, num2 - 3, numVals)], key= lambda x: abs(x))
        else:
            return sorted([math.floor(n) for n in linspace(num2 + 3, num1 - 3, numVals)], key= lambda x: abs(x))


    def _fillXRouteLeg(self, start, end, spaceVals):
        print(f"        -- {spaceVals}")
        leg = []

        if start.y == end.y or len(spaceVals) < 1:
            leg.append(PathPoint(start, end))
            return leg
        
        currPoint = PathPoint(start, Vec3(spaceVals[0], start.y, start.z))
        leg.append(currPoint)
        prevPoint = currPoint

        for val in spaceVals:
            # go down
            if abs(currPoint.start.y - end.y) < 3:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(
                        val + (abs(currPoint.start.y - end.y) * self.stepX),
                        prevPoint.end.y + (abs(currPoint.start.y - end.y) * self.stepY),
                        prevPoint.end.z
                    )
                )
            else:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(val + (3 * self.stepX), prevPoint.end.y + (3 * self.stepY),  prevPoint.end.z)
                )

            leg.append(currPoint)
            prevPoint = currPoint

            # then go straight
            if val == spaceVals[-1]:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(end.x, prevPoint.end.y,  prevPoint.end.z)
                )
            else:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(spaceVals[spaceVals.index(val) + 1], prevPoint.end.y,  prevPoint.end.z)
                )

            leg.append(currPoint)
            prevPoint = currPoint

        return leg

    
    def _fillZRouteLeg(self, start, end, spaceVals):
        print(f"        -- {spaceVals}")
        leg = []

        if start.y == end.y or len(spaceVals) < 1:
            leg.append(PathPoint(start, end))
            return leg

        currPoint = PathPoint(start, Vec3(start.x, start.y, spaceVals[0]))
        leg.append(currPoint)
        prevPoint = currPoint

        for val in spaceVals:
            # go down
            if abs(currPoint.start.y - end.y) < 3:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(
                        prevPoint.end.z,
                        prevPoint.end.y + (abs(currPoint.start.y - end.y) * self.stepY),
                        val + (abs(currPoint.start.y - end.y) * self.stepZ)
                    )
                )
            else:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(prevPoint.end.x, prevPoint.end.y + (3 * self.stepY),  val + (3 * self.stepZ))
                )

            leg.append(currPoint)
            prevPoint = currPoint

            # then go straight
            if val == spaceVals[-1]:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(prevPoint.end.x, prevPoint.end.y,  end.z)
                )
            else:
                currPoint = PathPoint(
                    prevPoint.end,
                    Vec3(prevPoint.end.x, prevPoint.end.y, spaceVals[spaceVals.index(val) + 1])
                )

            leg.append(currPoint)
            prevPoint = currPoint

        return leg


    #create list of PathPoints that represent the beginning and end of each section of the path
    #the path consists of 3 parts (50% of the first direction, the full second direction, the last part of the first direction)
    def planRoute(self):
        self._balanceStairNumbers()

        if self.xStairs < 0 and self.zStairs < 0:
            #for the time being while no solution for spiral staircase etc
            print("        -- !!Spiral staircase needed!!")
            return

        print(f"        -- Steps: {self.stepX}, {self.stepY}, {self.stepZ}")\

        if self.direction == Direction.EAST or self.direction == Direction.WEST:
            print("        -- X first")
            split1 = self.xStairs // 2 if self.xStairs % 2 == 0 else (self.xStairs // 2) + 1
            split2 = self.xStairs // 2
            self.leg1 = self._fillXRouteLeg(
                self.start, 
                Vec3(
                    self.start.x + (self.stepX * (abs(self.start.x - self.end.x) // 2)),
                    self.start.y + (self.stepY * (split1 * 3)),
                    self.start.z
                ),
                self._spaceValues(
                    self.start.x,
                    self.start.x + (self.stepX * (abs(self.start.x - self.end.x) // 2)),
                    split1
                )
            )

            self.leg2 = self._fillZRouteLeg(
                self.leg1[-1].end, 
                Vec3(
                    self.leg1[-1].end.x,
                    self.leg1[-1].end.y + (self.stepY * (self.zStairs * 3)),
                    self.end.z
                ),
                self._spaceValues(self.leg1[-1].end.z, self.end.z, self.zStairs)
            )

            self.leg3 = self._fillXRouteLeg(
                self.leg2[-1].end,
                self.end,
                self._spaceValues(self.leg2[-1].end.x, self.end.x, split2)
            )
        else:
            print("        -- Z first")
            split1 = self.zStairs // 2 if self.zStairs % 2 == 0 else (self.zStairs // 2) + 1
            split2 = self.zStairs // 2
            self.leg1 = self._fillZRouteLeg(
                self.start, 
                Vec3(
                    self.start.x,
                    self.start.y + (self.stepY * (split1 * 3)),
                    self.start.z + (self.stepZ * (abs(self.start.z - self.end.z) // 2))
                ),
                self._spaceValues(
                    self.start.z,
                    self.start.z + (self.stepZ * (abs(self.start.z - self.end.z) // 2)),
                    split1
                )
            )

            self.leg2 = self._fillXRouteLeg(
                self.leg1[-1].end, 
                Vec3(
                    self.end.x,
                    self.leg1[-1].end.y + (self.stepY * (self.zStairs * 3)),
                    self.leg1[-1].end.z
                ),
                self._spaceValues(self.leg1[-1].end.x, self.end.x, self.xStairs)
            )

            self.leg3 = self._fillZRouteLeg(
                self.leg2[-1].end,
                self.end,
                self._spaceValues(self.leg2[-1].end.z, self.end.z, split2)
            )


    