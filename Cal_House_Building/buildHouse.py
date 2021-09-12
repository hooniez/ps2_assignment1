import numpy as np
import random
class house_property:
    def __init__(self,location,width,depth):
        self.xstart = location.x+1 #starts 1x square away from player, can be changed later
        # print('xstart is',self.xstart)
        self.base = location.y-1 #starts -1y square away from player
        # print('base is',self.base)
        self.zstart = location.z+1 #starts 1z square away from player
        # print('zstart is',self.zstart)
        self.xend = location.x+width+1 #extends width +1 from player in x direction
        # print('xend is',self.xend)
        self.zend = location.z+depth+1 #extends width +1 from player in z direction
        # print('zend is',self.zend)
        self.width = width #to simplify future calculations
        self.depth = depth

    def drawProperty(self,mc): #creates a property of green grass can be removed later depending on if needed.
        mc.setBlocks(self.xstart,self.base,self.zstart,self.xend,self.base,self.zend,2)

class house2:
    def __init__(self,prop): 
        self.prop = prop #the property that the house exists on
        self.rooms = [] #list of all the room locations in the house

    def createEmptyHouse(self,roomheight,roomsize):
        propertyEdge = 1 #amount of space around the property before the rooms start
        self.roomheight = roomheight
        self.roomsperx = (self.prop.width - propertyEdge*2)//roomsize #calculates the number of rooms that will be created along the X direction
        self.roomsperz = (self.prop.depth - propertyEdge*2)//roomsize #calculates the number of rooms that will be created along the Z direction
        # print('roomsperx',self.roomsperx) #for testing
        # print('roomsperz',self.roomsperz) #for testing
        roomsizewidth = roomsize 
        roomsizedepth = roomsize
        for z in range(0,self.roomsperz): #following initalised empty rooms in an array. The rooms can later be filled with different types by calling functions in room2 class (may rename this class in future)
            for x in range(0,self.roomsperx):
                newSpace = room2(self.prop.xstart+(roomsizewidth*x)+propertyEdge,\
                                        self.prop.base,\
                                        self.prop.zstart+(roomsizedepth*z)+propertyEdge,\
                                        self.prop.xstart+(roomsizewidth*(x+1))+propertyEdge,\
                                        self.prop.base+self.roomheight,\
                                        self.prop.zstart+(roomsizewidth*(z+1))+propertyEdge,\
                                        x+(z*self.roomsperz),\
                                        x,z)
                self.setConnectedRooms(newSpace)
                print('connected rooms array',newSpace.connectedRooms)
                self.rooms.append(newSpace) #Coordinates of location in grid
        # print('rooms length is:',len(self.rooms)) #for testing
                
    def addRoom(self,mc,roomtype='basic'): #currently not in use
        empty = True
        builtRooms = []
        for room in self.rooms: #search through all rooms
            if room.full == True: #if a room exists (anything that isn't air. Pool is a room Room is a room etc)
                empty = False
                builtRooms.append(room) #add the room to the builtrooms working array
        if empty:
            currentRoom = self.rooms[random.randint(0,len(self.rooms)-1)] #If there are not yet any rooms select a random room as the starting room.
            # print('build a room at x = ',currentRoom.gridCoord[0], 'z = ',currentRoom.gridCoord[1])
            currentRoom.createRoom(mc,roomtype)
        else:
            roomIndex = random.randint(0,len(builtRooms)-1)
            # print(f'{roomIndex = }')
            fromRoom = builtRooms[roomIndex] #Select a room at random from the built rooms
            builtRooms.pop(roomIndex) #Remove this room from the builtRooms array
            # print('fromRoom tuple x = ',fromRoom.gridCoord[0], 'z = ',fromRoom.gridCoord[1])
            # print('in addRoom, length of builtRooms is:',len(builtRooms))
            availableRooms = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
            while len(availableRooms)==0: #while there are no avaliable room spaces select a new room to start search from
                if(len(builtRooms)==0): #No more rooms to build From
                    print('No more room space avaliable')
                    return None
                else:
                    roomIndex = random.randint(0,len(builtRooms)-1) #select another room at random
                    fromRoom = builtRooms[roomIndex]
                    builtRooms.pop(roomIndex)
                    availableRooms = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
            currentRoom = availableRooms[random.randint(0,len(availableRooms)-1)] #Select a room from avaliable Rooms at random
            # print('build a room at x = ',currentRoom.gridCoord[0], 'z = ',currentRoom.gridCoord[1])
            currentRoom.createRoom(mc,roomtype)


    def addDoors(self):
        for room in self.rooms: #search through all rooms
            if room.full: #if the full flag is true
                #check if the room has a door
                if(len(room.doorLocs)==0): #if no door
                    for connected in room.connectedRooms:
                        if connected: #if its not None
                            if connected.full: #if the connected Room is full
                                room.doorLocs.append[]
    # CONTINUE WORK ON ADD DOORS FUNCTION


    def setConnectedRooms(self,emptyRoom):
        arrayLocationX = emptyRoom.gridCoord[0]
        arrayLocationZ = emptyRoom.gridCoord[1]
        left = True
        right = True
        back = True
        front = True
        if(arrayLocationX == 0): #On left edge
            left = False
        if(arrayLocationX == self.roomsperx-1): #On right edge
            right = False
        if(arrayLocationZ == 0): #On the front edge
            front = False
        if(arrayLocationZ == self.roomsperz-1): #On back edge
            back = False
        if(left):
            emptyRoom.connectedRooms[0] = emptyRoom.roomPos - 1
        if(right):
            emptyRoom.connectedRooms[1] = emptyRoom.roomPos + 1
        if(front):
            emptyRoom.connectedRooms[2] = emptyRoom.roomPos - self.roomsperx
        if(back):
            emptyRoom.connectedRooms[3] = emptyRoom.roomPos + self.roomsperx


    def checkAvailableRooms(self,currentRoom):
        arrayLocationX = currentRoom.gridCoord[0]
        arrayLocationZ = currentRoom.gridCoord[1]
        availableRooms = []
        left = True
        right = True
        back = True
        front = True
        if(arrayLocationX == 0): #On left edge
            left = False
        if(arrayLocationX == self.roomsperx-1): #On right edge
            right = False
        if(arrayLocationZ == 0): #On the front edge
            front = False
        if(arrayLocationZ == self.roomsperz-1): #On back edge
            back = False
        #Checking if rooms exist in other locations in array
        if(left): #Location is not on the left edge so can -1 from location
            if(self.rooms[currentRoom.roomPos - 1].full == False): #This room is empty can build a room here
                availableRooms.append(self.rooms[currentRoom.roomPos - 1])
        if(right):
            if(self.rooms[currentRoom.roomPos + 1].full == False): #This room is empty can build a room here
                availableRooms.append(self.rooms[currentRoom.roomPos + 1])
        if(front):
            if(self.rooms[currentRoom.roomPos - self.roomsperx].full == False): #This room is empty can build a room here
                availableRooms.append(self.rooms[currentRoom.roomPos - self.roomsperx])
        if(back):
            if(self.rooms[currentRoom.roomPos + self.roomsperx].full == False): #This room is empty can build a room here
                availableRooms.append(self.rooms[currentRoom.roomPos + self.roomsperx])
        return availableRooms #list of avaliable indexs

class room2:
    def __init__(self,xstart,ystart,zstart,xend,yend,zend,roomPos,gridX,gridZ,type=0):
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xend = xend
        self.yend = yend #will normally hold room height
        self.zend = zend
        self.roomPos = roomPos #position in the rooms Array
        ## Add list of rooms that are connected left,right,front,back
        self.connectedRooms = [None,None,None,None]
        self.gridCoord = (gridX,gridZ)
        self.full = False
        self.doorLocs = []
    def createRoom(self,mc,roomtype):
        if(roomtype=='basic'):
            self.createBox(mc)
            self.emptyBox(mc)
            self.full = True
        if(roomtype=='pool'):
            self.createPool(mc)
    def createBox(self,mc): #Creates a box of blocks used in createRoom Func
        mc.setBlocks(self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend,7)
        #print('in createBox: ',self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend)
    def emptyBox(self,mc):  #Emptys the box of blocks used in createRoom
        mc.setBlocks(self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1,0)
        #print('in emptyBox: ',self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1)

    def createDoor(self,mc,doortype='single'):
        pass
        self.doorLocs.append((doorX,doorY,doorZ,doorWidth,doorHeight,doorDepth))
        mc.setBlocks(self.xstart+width//2,self.ystart,self.zstart,self.xstart+width//2+1,self.yend+3,self.zstart,2)

    def createPool(self,mc):
        pooldepth = 4
        boundrywidth = 1
        # mc.setBlocks(self.xstart,self.ystart,self.zstart,\
        #             self.xend,self.ystart,self.zend,24) #create outer pool shell boundry
        mc.setBlocks(self.xstart+boundrywidth,self.ystart,self.zstart+boundrywidth,\
                    self.xend-boundrywidth,self.ystart-pooldepth-1,self.zend-boundrywidth,1,2) #create pool shell
        mc.setBlocks(self.xstart+boundrywidth+1,self.ystart,self.zstart+boundrywidth+1,\
                    self.xend-boundrywidth-1,self.ystart-pooldepth,self.zend-boundrywidth-1,9) #create water

 