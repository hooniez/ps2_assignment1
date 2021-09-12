Week 1 Exercises:
Convert the binary number 10101 to decimal.
Answer: 21
Convert the hexadecimal number 3E to decimal.
Answer:62
Convert the binary number 1101 0010 1011 1111 to hexadecimal. (Hint: Break the binary digits into groups of 4.)
Answer: D2BF
Convert the decimal number 39 to binary.
Answer: 100111
Convert the decimal number 63 to hexadecimal (see here (Links to an external site.) for explanation of one algorithm).
Answer:3F

Week 1 Project:
- Working on developing my own implementation of build House.
- Orignally I was trying to develop a house with random and different room sizes but found it difficult to find a way to simple determine if a new room was next to a previous, this made implemenation of doors or windows impossible.
- Due to above issues decided to develop the house around the idea of mulitple zones, by dividing the block of land(property) into sections.
- This has the advantage of a wide variety of different house designs while still making implementation and modulation simple.
- Currently three seperate classes work together to create house,
- house_property class: Which holds information about the entire property
- house2 class, holds information and functions related to the house sepcifically.
- room2 class, which holds infromation and functions related to rooms(also includes pools and other types), including drawing methods.
- I have also been working on improving my code commenting and explinations to help my team understand what I am working on.
- Although the current implementation is not complete I am happy with how it is progressing at this point.

A the time of creating this Diary The code can be seen below. Note that this code is not fully functional at this point and in this form. A more functional version can be accessed from the git_hub.
class house_property:
    def __init__(self,location,width,depth):
        self.xstart = location.x+1 #starts 1x square away from player, can be changed later
        print('xstart is',self.xstart)
        self.base = location.y-1 #starts -1y square away from player
        print('base is',self.base)
        self.zstart = location.z+1 #starts 1z square away from player
        print('zstart is',self.zstart)
        self.xend = location.x+width+1 #extends width +1 from player in x direction
        print('xend is',self.xend)
        self.zend = location.z+depth+1 #extends width +1 from player in z direction
        print('zend is',self.zend)
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
        print('roomsperx',self.roomsperx) #for testing
        print('roomsperz',self.roomsperz) #for testing
        roomsizewidth = roomsize 
        roomsizedepth = roomsize
        for z in range(0,self.roomsperz): #following initalised empty rooms in an array. The rooms can later be filled with different types by calling functions in room2 class (may rename this class in future)
            for x in range(0,self.roomsperx):
                self.rooms.append(room2(self.prop.xstart+(roomsizewidth*x)+propertyEdge,\
                                        self.prop.base,\
                                        self.prop.zstart+(roomsizedepth*z)+propertyEdge,\
                                        self.prop.xstart+(roomsizewidth*(x+1))+propertyEdge,\
                                        self.prop.base+self.roomheight,\
                                        self.prop.zstart+(roomsizewidth*(z+1))+propertyEdge,\
                                        x+(z*roomsperz),\
                                        x,z)) #Position in the rooms array
                                            

        print('rooms length is:',len(self.rooms)) #for testing



/// CURRENTLY WORKING ON THE FOLLOWING FUNCTIONS AT POINT OF WRITING ///

    def addRoom(self,mc,type='basic'): #currently not in use
        pass
        empty = True
        builtrooms = []
        for room in self.rooms: #search through all rooms
            if room.full == True: #if a room exists (anything that isn't air. Pool is a room Room is a room etc)
                empty = False
                builtrooms.append(room) #add the room to the builtrooms working array
        if empty:
            currentRoom = self.rooms[random.randint(0,len(self.rooms)-1)] #If there are not yet any rooms select a random room as the starting room.
            currentRoom.createRoom(mc)
            self.setAvaliable(currentRoom,rooms)
        else:
            fromRoom = builtrooms[random.randint(0,len(builtrooms)-1)] #Select a room at random from the built rooms
            #Select an empty space next to the fromRoom
            self.checkAvaliable
            arrayLocation = fromRoom.roomPos
            #Check locations around the room


            x+z*roomsperz
            random.randint(0, 3) #4 possible room locations 0,1,2,3
            
    def setAvaliable(self,currentRoom,rooms):
        if(arrayLocation-1 < 0): #outside the array
                pass
    def checkAvaliable(self,currentRoom,rooms):
        arrayLocation = current.roomPos
        left = arrayLocation-1
        right = arrayLocation+1
        top = arrayLocation
        bot = arrayLocation
        if(arrayLocation-1 >= 0): #this is in the array
            rooms[arrayLocation]

        return #list of avaliable indexs

/// FINISH WORKING ON FUNCTIONS ///


class room2:
    def __init__(self,xstart,ystart,zstart,xend,yend,zend,roomPos,gridX,gridZ,type=0):
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xend = xend
        self.yend = yend #will normally hold room height
        self.zend = zend
        self.roomPos = roomPos
        self.gridCoord = (gridX,gridZ)
        self.full = False
    def createRoom(self,mc):
        self.createBox(mc)
        self.emptyBox(mc)
        self.full = True
    def createBox(self,mc): #Creates a box of blocks used in createRoom Func
        mc.setBlocks(self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend,7)
        #print('in createBox: ',self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend)
    def emptyBox(self,mc):  #Emptys the box of blocks used in createRoom
        mc.setBlocks(self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1,0)
        #print('in emptyBox: ',self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1)

    def createPool(self,mc):
        pooldepth = 4
        boundrywidth = 1
        mc.setBlocks(self.xstart,self.ystart,self.zstart,\
                    self.xend,self.ystart,self.zend,24) #create outer pool shell boundry
        mc.setBlocks(self.xstart+boundrywidth,self.ystart,self.zstart+boundrywidth,\
                    self.xend-boundrywidth,self.ystart-pooldepth-1,self.zend-boundrywidth,1,2) #create pool shell
        mc.setBlocks(self.xstart+boundrywidth+1,self.ystart,self.zstart+boundrywidth+1,\
                    self.xend-boundrywidth-1,self.ystart-pooldepth,self.zend-boundrywidth-1,9) #create water