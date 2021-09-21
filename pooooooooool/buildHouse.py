#<<<<<<< HEAD
#=======
#import numpy as np
import random
import buildMain
class house_property:
    def __init__(self,location,width,depth):
        self.xstart = location.x+1 #starts 1x square away from player, can be changed later
        self.base = location.y-1 #starts -1y square away from player
        self.zstart = location.z+1 #starts 1z square away from player
        self.xend = location.x+width+1 #extends width +1 from player in x direction
        self.zend = location.z+depth+1 #extends width +1 from player in z direction
        self.width = width #to simplify future calculations
        self.depth = depth
        self.propertyEdge = 2

    def drawProperty(self,mc): #creates a property of green grass can be removed later depending on if needed.
        mc.setBlocks(self.xstart,self.base,self.zstart,self.xend,self.base,self.zend,2)

class house: #this is a house class has an array of floors 
    def __init__(self,prop,floorHeight,roomSize):
        self.prop = prop #the property
        self.floors = [] #all the house levels
        self.floorHeight = floorHeight
        self.roomSize = roomSize
        self.propertyEdge = prop.propertyEdge

    def createFloor(self):
        if len(self.floors) == 0: #this is the first floor, so use default
            newFloor = floor(self.prop)
            newFloor.createEmptyFloor(self.propertyEdge,None,0,self.floorHeight,self.roomSize) #There is no below floor
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
            newFloor = floor(self.prop)
            newFloor.createEmptyFloor(
                                    self.propertyEdge,belowFloor,
                                    len(self.floors),
                                    self.floorHeight,
                                    self.roomSize
                                    )
            self.floors.append(newFloor)

    def addAllStairs(self,mc):
        for floor in self.floors:
            floor.addStairs(mc)

    def addAllWindows(self,mc):
        for floor in self.floors:
            floor.addWindows(mc)
 

class floor: #new class for floors
    def __init__(self,prop): 
        self.prop = prop #the property that the house exists on
        self.rooms = [] #list of all the room locations in the house
        self.roomOrder = [] #order that rooms are place in the house
        #to imagine grid layout as array indexs
        ################
        #   2 | 5 | 8
        # x 1 | 4 | 7
        #   0 | 3 | 6
        #       z
        ################

    def createEmptyFloor(self,propertyEdge,belowFloor,floorLevel,floorHeight,roomsize):
        self.floorLevel = floorLevel
        self.belowFloor = belowFloor
        self.floorHeight = floorHeight
        self.roomsperx = (self.prop.width - propertyEdge*2)//roomsize #calculates the number of rooms that will be created along the X direction
        self.roomsperz = (self.prop.depth - propertyEdge*2)//roomsize #calculates the number of rooms that will be created along the Z direction
        roomsizewidth = roomsize 
        roomsizedepth = roomsize
        for z in range(0,self.roomsperz): #following initalised empty rooms in an array. The rooms can later be filled with different types by calling functions in room class
            for x in range(0,self.roomsperx):
                newSpace = room(
                                self.prop.xstart+(roomsizewidth*x)+propertyEdge,
                                self.prop.base+(floorHeight*floorLevel),
                                self.prop.zstart+(roomsizedepth*z)+propertyEdge,
                                self.prop.xstart+(roomsizewidth*(x+1))+propertyEdge,
                                self.prop.base+self.floorHeight+(floorHeight*floorLevel),
                                self.prop.zstart+(roomsizedepth*(z+1))+propertyEdge,
                                x+(z*self.roomsperz),
                                x,z
                                ) #coordinates in the grid
                self.setConnectedRooms(newSpace)
                self.rooms.append(newSpace) #Coordinates of location in grid
    def addRoom(self,mc,roomtype='basic'):
        empty = True
        builtRooms = []
        avaliableRooms = []
        if(roomtype == 'pool' and self.floorLevel != 0):
            print('Can only add pool to ground floor, room not added')
            return
        #first check if we are the ground Floor
        if self.belowFloor == None: #we are at the ground floor
            avaliableRooms = self.rooms #All rooms are avaliable
        else: #if there is a below floor, then we need to ask that floor for a list of builable locations
            for room in self.belowFloor.rooms:
                if room.buildUpAvaliablity == True: #A room can be built up from
                    avaliableRooms.append(self.rooms[room.roomPos]) #add to the avaliableRooms array
        if len(avaliableRooms) == 0: #No avaliable rooms
            print('No avaliable room positions at level:',self.floorLevel)
        else:
            for room in avaliableRooms: #search through all rooms
                if room.full == True: #if a room exists (anything that isn't air. Pool is a room Room is a room etc)
                    empty = False
                    builtRooms.append(room) #add the room to the builtrooms working array
            if empty:
                currentRoom = avaliableRooms[random.randint(0,len(avaliableRooms)-1)] #If there are not yet any rooms select a random room as the starting room.
                currentRoom.createRoom(mc,roomtype)
                self.roomOrder.append((currentRoom.roomPos,None))
            else:
                roomIndex = random.randint(0,len(builtRooms)-1)
                fromRoom = builtRooms[roomIndex] #Select a room at random from the built rooms
                builtRooms.pop(roomIndex) #Remove this room from the builtRooms array
                builable = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
                while len(builable)==0: #while there are no avaliable room spaces select a new room to start search from
                    if(len(builtRooms)==0): #No more rooms to build From
                        print('No more room space avaliable')
                        return None
                    else:
                        roomIndex = random.randint(0,len(builtRooms)-1) #select another room at random
                        fromRoom = builtRooms[roomIndex]
                        builtRooms.pop(roomIndex)
                        builable = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
                randNum = random.randint(0,len(builable)-1) #room select to create that connects to the current Room
                currentRoom = builable[randNum] #Select a room from avaliable Rooms at random
                currentRoom.createRoom(mc,roomtype)
                self.roomOrder.append((currentRoom.roomPos,fromRoom.roomPos))
            
    def addDoors(self, mc):
        for index in range(len(self.roomOrder)): #the position of the first room in rooms list
            if(self.roomOrder[index][1]!=None): #if its not the first room
                self.rooms[self.roomOrder[index][0]].createDoor(mc,self.rooms[self.roomOrder[index][1]]) #create a door between this room
            else: #its the first room, send in None
                self.rooms[self.roomOrder[index][0]].createDoor(mc,None)

    def addFrontDoor(self, mc):
        for room in self.rooms: #search through all the rooms, add a door to the first full room
            if room.full: #this room is a full room
                room.walls[2] = 2 #There is a door in the left position (2). Store it in the doors array
                room.drawDoor(mc,2,'single')
                break 
    
    def addStairs(self,mc):
        if(self.belowFloor == None): #If we are at the ground level
            #don't build any stairs
            pass
        else: #We at a level 1->
            avaliableRooms = []
            for room in self.rooms:
                if room.full==True: #The room is full
                    avaliableRooms.append(room.roomPos) #add to list of avaliable Rooms
            randIndex = random.randint(0,len(avaliableRooms)-1) #select a random index from the avaliableRooms array
            currentRoom = self.rooms[avaliableRooms[randIndex]] #set the current room to the value at this index
            belowRoom = self.belowFloor.rooms[avaliableRooms[randIndex]]
            avaliableRooms.pop(randIndex) #remove this value from the avaliable Rooms
            avaliableSpace = currentRoom.findSpaceOnRoomWalls(belowRoom)
            while len(avaliableSpace) == 0: #while their is no avaliable space
                if(len(avaliableRooms) == 0): #check if their is any more possible rooms
                    return
                else:
                    randIndex = random.randint(0,len(avaliableRooms)-1) #select a random index from the avaliableRooms array
                    currentRoom = self.rooms[avaliableRooms[randIndex]] #set the current room to the value at this index
                    belowRoom = self.belowFloor.rooms[avaliableRooms[randIndex]]
                    avaliableRooms.pop(randIndex) #remove this value from the avaliable Rooms
                    avaliableSpace = currentRoom.findSpaceOnRoomWalls(belowRoom)
            else:
                randSpace = random.randint(0,len(avaliableSpace)-1) #select a space at random
                currentRoom.createStaircase(mc,belowRoom,avaliableSpace[randSpace])

    def addWindows(self,mc):
        for currentRoom in self.rooms: #Search through all the rooms
            if currentRoom.full == True: #The room is filled
                print(f'{currentRoom.roomPos=}')
                print(f'{currentRoom.roomPos} has empty wall space at {currentRoom.walls}')
                for index, conRoom in enumerate(currentRoom.connectedRooms): #look at the connected rooms:
                    if conRoom != None: #If there is no room there potential window Location
                        if self.rooms[conRoom].full == False:
                            if(currentRoom.walls[index] == None):
                                currentRoom.createWindow(mc,index)
                    else:
                        if(currentRoom.walls[index] == None):
                            currentRoom.createWindow(mc,index)
                        #do nothing

        pass


    def setConnectedRooms(self,emptyRoom):
        arrayLocationX = emptyRoom.gridCoord[0]
        arrayLocationZ = emptyRoom.gridCoord[1]
        left = True
        right = True
        back = True
        front = True
        if(arrayLocationX == 0): #On bot edge
            left = False
        if(arrayLocationX == self.roomsperx-1): #On top edge
            right = False
        if(arrayLocationZ == 0): #On the left edge
            front = False
        if(arrayLocationZ == self.roomsperz-1): #On right edge
            back = False
        if(left):
            emptyRoom.connectedRooms[0] = emptyRoom.roomPos - 1
        if(right):
            emptyRoom.connectedRooms[1] = emptyRoom.roomPos + 1
        if(front):
            emptyRoom.connectedRooms[2] = emptyRoom.roomPos - self.roomsperx
        if(back):
            emptyRoom.connectedRooms[3] = emptyRoom.roomPos + self.roomsperx

    # Check if a room is avaliable to build on floor.
    def checkAvailableRooms(self,currentRoom):
        arrayLocationX = currentRoom.gridCoord[0]
        arrayLocationZ = currentRoom.gridCoord[1]
        availableRooms = []
        bot = True
        top = True
        left = True
        right = True
        if(arrayLocationX == 0): #On bot edge
            bot = False
        if(arrayLocationX == self.roomsperx-1): #On top edge
            top = False
        if(arrayLocationZ == 0): #On the left edge
            left = False
        if(arrayLocationZ == self.roomsperz-1): #On right edge
            right = False
        #Checking if rooms exist in other locations in array
        if bot: #Location is not on the left edge so can -1 from location
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos - 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - 1])
            elif self.belowFloor.rooms[currentRoom.roomPos - 1].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos - 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - 1])
        if top:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos + 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + 1])
            elif self.belowFloor.rooms[currentRoom.roomPos + 1].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos + 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + 1])
        if left:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos - self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - self.roomsperx])
            elif self.belowFloor.rooms[currentRoom.roomPos - self.roomsperx].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos - self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - self.roomsperx])
        if right:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos + self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + self.roomsperx])
            elif self.belowFloor.rooms[currentRoom.roomPos + self.roomsperx].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos + self.roomsperx].full == False:                    
                    availableRooms.append(self.rooms[currentRoom.roomPos + self.roomsperx])
        return availableRooms #list of avaliable indexs

class room:
    def __init__(self,xstart,ystart,zstart,xend,yend,zend,roomPos,gridX,gridZ,type=0):
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xend = xend
        self.yend = yend #will normally hold room height
        self.zend = zend
        self.roomPos = roomPos #position in the rooms Array
        ## Add list of rooms that are connected bot,top,left,right
        ##
        ##              Top      
        ##           ________
        ## Left     |        |     Right
        ##        X |        |
        ##          |________|
        ##              Z
        ##              Bot

        self.connectedRooms = [None,None,None,None] #bot,top,left,right
        self.gridCoord = (gridX,gridZ)
        self.full = False #Room does not exist by default
        self.roomType = 'none'
        self.buildUpAvaliablity = False
        self.walls = [None,None,None,None] #bot,top,left,right

    def createRoom(self,mc,roomtype):
        if(roomtype=='basic'):
            self.roomType = 'basic'
            self.createBox(mc)
            self.emptyBox(mc)
            self.full = True #There is now something in the room
            self.buildUpAvaliablity = True
        if(roomtype=='pool'):
            self.roomType = 'pool'
            self.createPool(mc)
            self.full = True #There is now something in the room
            self.buildUpAvaliablity = False
            
    def createBox(self,mc): #Creates a box of blocks used in createRoom Func
        mc.setBlocks(
                    self.xstart,
                    self.ystart,
                    self.zstart,
                    self.xend,
                    self.yend,
                    self.zend,
                    35,
                    self.roomPos+1
        ) #Room Color Selection
    def emptyBox(self,mc):  #Emptys the box of blocks used in createRoom
        mc.setBlocks(
                    self.xstart+1,
                    self.ystart+1,
                    self.zstart+1,
                    self.xend-1,
                    self.yend-0,
                    self.zend-1,
                    0
                    )

    def createDoor(self,mc,prevRoom,doortype='single'):
        if(prevRoom is None): #Do nothing
            pass
        else: #Previous room exists, 
            currentLocation = self.connectedRooms.index(prevRoom.roomPos) #find index of prevRoom room in the prevRoom room connectedRooms array
            self.walls[currentLocation] = currentLocation
            doorLocationPrev = prevRoom.connectedRooms.index(self.roomPos) #find index of current room in the prevRoom room connectedRooms array
            prevRoom.walls[doorLocationPrev] = doorLocationPrev
            self.drawDoor(mc,currentLocation, doortype)
    
    # Start implementation of staircase
    def createStaircase(self,mc,belowRoom,randSpace): #belowroom holds the room below
        stairWidth = 2 #these are hard coded but could be changed to be given as inputs to the function at a later date
        wallWidth = 1
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        roomHeight = abs(self.ystart-self.yend)
        #door is on bot
        if(randSpace == 0):
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xstart+1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+i+1,
                            belowRoom.xstart+stairWidth,
                            belowRoom.ystart+i,
                            belowRoom.zstart+roomHeight+1,
                            45
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xstart+1,
                        belowRoom.yend,
                        belowRoom.zstart+2,\
                        belowRoom.xstart+stairWidth,
                        belowRoom.yend,
                        belowRoom.zend+(roomHeight-roomDepth),
                        0 #air
                        )

        #door is on top
        if(randSpace == 1):
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xend-1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+i+1,
                            belowRoom.xend-stairWidth,
                            belowRoom.ystart+i,
                            belowRoom.zstart+roomHeight+1,
                            45
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xend-1,
                        belowRoom.yend,
                        belowRoom.zstart+2,
                        belowRoom.xend-stairWidth,
                        belowRoom.yend,
                        belowRoom.zend+(roomHeight-roomDepth),
                        0 #air
                        )
        #door is on left
        if(randSpace == 2):
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xstart+i+1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+1,
                            belowRoom.xstart+roomHeight+1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+stairWidth,
                            45
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xstart+2,
                        belowRoom.yend,
                        belowRoom.zstart+1,
                        belowRoom.xend+(roomHeight-roomWidth),
                        belowRoom.yend,
                        belowRoom.zstart+stairWidth,
                        0
                        )
        #door is on right
        if(randSpace == 3):
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xstart+i+1,
                            belowRoom.ystart+i,
                            belowRoom.zend-1,
                            belowRoom.xstart+roomHeight+1,
                            belowRoom.ystart+i,
                            belowRoom.zend-stairWidth,
                            45
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xstart+2,
                        belowRoom.yend,
                        belowRoom.zend-1,
                        belowRoom.xend+(roomHeight-roomWidth),
                        belowRoom.yend,
                        belowRoom.zend-stairWidth,
                        0
                        )

        belowRoom.walls[randSpace] = randSpace #Set the doors array to the new space
        self.walls[randSpace] = randSpace
    
    def drawDoor(self,mc,doordirection,doortype):
        doorWidth = 1 #these are hard coded but could be changed to be given as inputs to the function at a later date
        doorDepth = 1
        doorHeight = 3
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        if(doordirection == 0): #door is on bot
            mc.setBlocks(
                self.xstart-doorDepth,
                self.ystart+1,
                self.zstart+roomDepth//2,
                self.xstart+doorDepth,
                self.ystart+doorHeight,
                self.zstart+roomDepth//2+doorWidth,
                0) #Acacia Wood Plank
        if(doordirection == 1): #door is on top
            mc.setBlocks(self.xend+doorWidth,self.ystart+1,self.zstart+roomDepth//2,self.xend-doorWidth,self.ystart+doorHeight,self.zstart+roomDepth//2+doorWidth,0) #Coarse Dirt
        if(doordirection == 2): #door is on left
            mc.setBlocks(self.xstart+roomDepth//2,self.ystart+1,self.zstart-doorWidth,self.xstart+roomDepth//2+doorWidth,self.ystart+doorHeight,self.zstart+doorWidth,0) #Granite
        if(doordirection == 3): #door is on right
            mc.setBlocks(self.xstart+roomDepth//2,self.ystart+1,self.zend-doorWidth,self.xstart+roomDepth//2+doorWidth,self.ystart+doorHeight,self.zend+doorWidth,0) #Polished Diorite

    # MUST IMPLEMENT CHANGES TO PREVENT POOL CREATION ON ANYTHING OTHER THAN GROUND LEVEL
    def createPool(self,mc):
        pooldepth = 4
        boundrywidth = 2
        mc.setBlocks(
                    self.xstart+boundrywidth,
                    self.ystart,
                    self.zstart+boundrywidth,
                    self.xend-boundrywidth,
                    self.ystart-pooldepth-1,
                    self.zend-boundrywidth,
                    1,
                    2
                    ) #create pool shell
        mc.setBlocks(
                    self.xstart+boundrywidth+1,
                    self.ystart,
                    self.zstart+boundrywidth+1,
                    self.xend-boundrywidth-1,
                    self.ystart-pooldepth,
                    self.zend-boundrywidth-1,
                    9
                    ) #create water

    def findSpaceOnRoomWalls(self,belowRoom):
        #Check if the below room has space for a staircase:
        belowSpace = belowRoom.walls #get the location of doors
        currentSpace = self.walls #get the location of doors
        avaliableSpace = []
        for i in range(len(currentSpace)):
            if (currentSpace[i] == None) and (belowSpace[i] == None): #this slot is avaliable
                avaliableSpace.append(i)
        return avaliableSpace

    def createWindow(self,mc,windowLoc):
        print('In create Window')
        print('windowLoc is',windowLoc)
        wallWidth = 1
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        roomHeight = abs(self.ystart-self.yend)
        if(windowLoc == 0): #bot
            mc.setBlocks(
                        self.xstart,
                        self.ystart+roomHeight//2,
                        self.zstart+roomDepth//4,
                        self.xstart,
                        self.yend-roomHeight//2,
                        self.zend-roomDepth//4,
                        20
                        )
        if(windowLoc == 1): #top
            mc.setBlocks(
                        self.xend,
                        self.ystart+roomHeight//2,
                        self.zstart+roomDepth//4,
                        self.xend,
                        self.yend-roomHeight//2,
                        self.zend-roomDepth//4,
                        20
                        )
        if(windowLoc == 2): #left
            mc.setBlocks(
                        self.xstart+roomWidth//4,
                        self.ystart+roomHeight//2,
                        self.zstart,
                        self.xend-roomWidth//4,
                        self.yend-roomHeight//2,
                        self.zstart,
                        20
                        )
        if(windowLoc == 3): #right
            mc.setBlocks(
                        self.xstart+roomWidth//4,
                        self.ystart+roomHeight//2,
                        self.zend,
                        self.xend-roomDepth//4,
                        self.yend-roomHeight//2,
                        self.zend,
                        20
                        )
#>>>>>>> bf578e6e2d504ee5847a66c8bf4c1dc93ab879f4

class pool:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z



    def digPool(self,mc):
        self.findEdge(30,30,mc)

        if self.poolRefRight == True: # if the pool is on the back right, it will build back and to the right
            #mc.setBlocks(self.x,self.y,self.z,self.x,self.y+1,self.z,0)
            self.x -=1
            self.z +=3
            self.y -=1
            mc.setBlocks(self.x,self.y,self.z,self.x-6,self.y-5,self.z+10,1)#stone outline
            mc.setBlocks(self.x,self.y+1,self.z,self.x-6,self.y+1,self.z+10,85)#fences
            mc.setBlocks(self.x-1,self.y+1,self.z,self.x-5,self.y+1,self.z+9,0)#air
            mc.setBlocks(self.x-1,self.y,self.z+1,self.x-5,self.y-4,self.z+9,9)#water
        elif self.poolRefRight == False: # if the pool is on the back right, it will build back and to the left
            #mc.setBlocks(self.x-1,self.y,self.z,self.x-1,self.y+1,self.z,0)
            self.x +=1
            self.z +=2
            self.y -=1
            mc.setBlocks(self.x,self.y,self.z,self.x+6,self.y-5,self.z+10,1)#stone outline
            mc.setBlocks(self.x,self.y+1,self.z,self.x+6,self.y+1,self.z+10,85)#fences
            mc.setBlocks(self.x+1,self.y+1,self.z,self.x+5,self.y+1,self.z+9,0)#air
            mc.setBlocks(self.x+1,self.y,self.z+1,self.x+5,self.y-4,self.z+9,9)#water
        

    def findPool(self,mc):
        room = buildMain.house.floor.room
        print(room.connectedRooms,"hi")
        #for i in room.connectedRooms:
         #   if i == None:
          #      if (mc.getBlocks(self.x,self.y,self.z,self.x+10,self.y,self.z+6) == 0 and
           #         mc.getBlocks(self.x,self.y-1,self.z,self.x+10,self.y-1,self.z+6) == 2):
            #        return self.x,self.y,self.z
