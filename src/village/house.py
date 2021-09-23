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
        self.roomX = 14
        self.roomZ = 10
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

    
    def generateHouse(self, mc):
        floorColor = random.randint(0, 15)
        self.createFloor(floorColor) # specify the room size, currently only squares
        self.floors[0].addRoom(mc)
        self.floors[0].addRoom(mc)
        self.floors[0].addRoom(mc)
        self.floors[0].addRoom(mc)
        self.floors[0].addRoom(mc,'pool')
        self.floors[0].addRoom(mc,'pool')
        print('---------')

        floorColor = random.randint(0, 15)
        self.createFloor(floorColor) 
        self.floors[1].addRoom(mc)
        self.floors[1].addRoom(mc)

        self.floors[1].addRoom(mc)

        floorColor = random.randint(0, 15)
        self.createFloor(floorColor)
        self.floors[2].addRoom(mc)

        self.addAllDoors(mc)
        self.floors[0].addFrontDoor(mc)
        self.addAllStairs(mc)
        self.addAllWindows(mc)
        # self.addFurniture(mc)
        self.addAllRoofs(mc)
        self.connectAllPools(mc)
        self.addAllFurniture(mc)


# Used for testing 
if __name__ == '__main__':
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    import random
    mc = minecraft.Minecraft.create()
    p = mc.player.getTilePos()

    houseLocation = p
    prop = Property(p,40,40) #boarder is 2 on each side so total of 4
    prop.drawProperty(mc)
    floorColor = random.randint(0, 15) #Uses wool block to draw House, wool block has 15 possible Colors
    myHouse = House(prop)

    myHouse.createFloor(floorColor) # specify the room size, currently only squares
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc,'pool')
    myHouse.floors[0].addRoom(mc,'pool')
    print('---------')

    floorColor = random.randint(0, 15)
    myHouse.createFloor(floorColor) 
    myHouse.floors[1].addRoom(mc)
    myHouse.floors[1].addRoom(mc)

    myHouse.floors[1].addRoom(mc)

    floorColor = random.randint(0, 15)
    myHouse.createFloor(floorColor)
    myHouse.floors[2].addRoom(mc)
    # myHouse.floors[2].addRoom(mc)
    # myHouse.floors[2].addRoom(mc)

    # floorColor = random.randint(0, 15)
    # myHouse.createFloor(floorColor)
    # myHouse.floors[3].addRoom(mc)
    # myHouse.floors[3].addRoom(mc)
    # myHouse.floors[3].addRoom(mc)

    # floorColor = random.randint(0, 15)
    # myHouse.createFloor(floorColor)
    # myHouse.floors[4].addRoom(mc)
    # myHouse.floors[4].addRoom(mc)

    # floorColor = random.randint(0, 15)
    # myHouse.createFloor(floorColor)
    # myHouse.floors[5].addRoom(mc)
    # myHouse.floors[5].addRoom(mc)

    myHouse.addAllDoors(mc)
    myHouse.floors[0].addFrontDoor(mc)
    myHouse.addAllStairs(mc)
    myHouse.addAllWindows(mc)
    # myHouse.addFurniture(mc)
    myHouse.addAllRoofs(mc)
    myHouse.connectAllPools(mc)
    myHouse.addAllFurniture(mc)