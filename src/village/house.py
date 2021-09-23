import random
from floor import Floor
from land import Property
from mcpi.vec3 import Vec3


class House: #this is a house class has an array of floors
    def __init__(self,prop):
        self.prop = prop #the property
        self.floors = [] #all the house levels
        self.floorHeight = 5
        self.roomSize = 10
        self.roomX = 12 ##Random
        self.roomZ = 10 #Random
        self.propertyEdge = 2

    def createFloor(self, floorColor):
        if len(self.floors) == 0: #this is the first floor, so use default
            newFloor = Floor(self.prop,floorColor)
            newFloor.createEmptyFloor(self.propertyEdge,None,0,self.floorHeight,self.roomX,self.roomZ) #There is no below floor
            self.floors.append(newFloor)
        else: # their is already a previous floor
            belowFloor = self.floors[-1] #select the last floor in floors array
            # check that the upper floor isn't empty:
            if len(belowFloor.roomOrder)==0: #all the rooms on the upperFloor are empty
                print('No Rooms avaliable on level', len(self.floors))
                return
            else:
                for room in belowFloor.rooms: #go through all the rooms #this can be sped up by instead foing throgh roomsOrder array
                    if room.buildUpAvaliablity == True:
                        #at least one room can be built off
                        break
            newFloor = Floor(self.prop, floorColor)
            newFloor.createEmptyFloor(self.propertyEdge,belowFloor,len(self.floors),self.floorHeight,self.roomX,self.roomZ)
            self.floors.append(newFloor)

    def addAllStairs(self,mc):
        for floor in self.floors:
            floor.addStairs(mc)

    def addAllWindows(self,mc):
        for floor in self.floors:
            floor.addWindows(mc)

    def addAllRoofs(self,mc):
        for floor in self.floors:
            floor.addRoof(mc)

    def addFurniture(self,mc):
        for floor in self.floors:
            floor.addFurniture(mc)

    def addAllDoors(self,mc):
        for floor in self.floors:
            floor.addDoors(mc)

    def connectAllPools(self,mc):
        if len(self.floors) > 0:
            self.floors[0].connectPools(mc)

    def addAllFurniture(self,mc):
        for floor in self.floors:
            floor.addFurnitureCal(mc)

    def addAllGarden(self,mc):
        if len(self.floors) > 0:
            self.floors[0].fillGardens(mc)

    
    def generateHouse(self, mc):
        Ztotal = 1
        Xtotal = 1
        if (self.prop.width-self.propertyEdge*2)//4 >= 10:
            Xtotal = 4
            self.roomX = (self.prop.width-self.propertyEdge*2)//4
        elif (self.prop.width-self.propertyEdge*2)//3 >= 10:
            Xtotal = 3
            self.roomX = (self.prop.width-self.propertyEdge*2)//3
        elif (self.prop.width-self.propertyEdge*2)//2 >= 10:
            Xtotal = 2
            self.roomX = (self.prop.width-self.propertyEdge*2)//2
        else:
            Xtotal = 1
            self.roomX = 10
            print('1*Z house')
        if (self.prop.depth-self.propertyEdge*2)//4 >= 10:
            Ztotal = 4
            self.roomZ = (self.prop.depth-self.propertyEdge*2)//4
        elif (self.prop.depth-self.propertyEdge*2)//3 >= 10:
            Ztotal = 3
            self.roomZ = (self.prop.depth-self.propertyEdge*2)//3
        elif (self.prop.depth-self.propertyEdge*2)//2 >= 10:
            Ztotal = 2
            self.roomZ = (self.prop.depth-self.propertyEdge*2)//2
        else:
            Ztotal = 1
            self.roomZ = 10
            print('X*1 house')
        maxHeight = 3
        total = Ztotal * Xtotal
        for m in range(0,maxHeight):
            counter = 0
            floorColor = random.randint(0, 15)
            self.createFloor(floorColor) # specify the room size, currently only squares
            for i in range(total//2,total):
                self.floors[m].addRoom(mc)
                counter+=1
            if m == 0:
                for i in range(1,1+total//4): #total-counter
                    self.floors[m].addRoom(mc,'pool')
            total = counter
        self.addAllDoors(mc)
        self.floors[0].addFrontDoor(mc)
        self.addAllStairs(mc)
        self.addAllWindows(mc)
        # self.addFurniture(mc)
        self.addAllRoofs(mc)
        self.connectAllPools(mc)
        self.addAllFurniture(mc)
        self.addAllGarden(mc)


# Used for testing 
if __name__ == '__main__':
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    import random
    mc = minecraft.Minecraft.create()
    p = mc.player.getTilePos()

    houseLocation = p
    prop = Property(p,48,48) #boarder is 2 on each side so total of 4
    prop.drawProperty(mc)
    floorColor = random.randint(0, 15) #Uses wool block to draw House, wool block has 15 possible Colors
    myHouse = House(prop)

    myHouse.generateHouse(mc)