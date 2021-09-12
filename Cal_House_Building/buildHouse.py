import numpy as np
import random
class house_property:
    def __init__(self,location,width,depth):
        self.xstart = location.x+1
        print('xstart is',self.xstart)
        self.base = location.y-1
        print('base is',self.base)
        self.zstart = location.z+1
        print('zstart is',self.zstart)
        self.xend = location.x+width+1
        print('xend is',self.xend)
        self.zend = location.z+depth+1
        print('zend is',self.zend)
        self.width = width
        self.depth = depth

    def drawProperty(self,mc): #creates a property of green grass can be removed later depending on if needed.
        mc.setBlocks(self.xstart,self.base,self.zstart,self.xend,self.base,self.zend,2)

class house2:
    def __init__(self,prop):
        self.prop = prop
        self.rooms = []

    def createEmptyHouse(self,roomheight,roomsize):
        propertyEdge = 1 #amount of space around the property before the rooms start
        self.roomheight = roomheight
        self.roomsperx = (self.prop.width - propertyEdge*2)//roomsize
        self.roomsperz = (self.prop.depth - propertyEdge*2)//roomsize
        print('roomsperx',self.roomsperx)
        print('roomsperz',self.roomsperz)
        roomsizewidth = roomsize
        roomsizedepth = roomsize
        for z in range(0,self.roomsperz):
            for x in range(0,self.roomsperx):
                self.rooms.append(room2(self.prop.xstart+(roomsizewidth*x)+propertyEdge,\
                                        self.prop.base,\
                                        self.prop.zstart+(roomsizedepth*z)+propertyEdge,\
                                        self.prop.xstart+(roomsizewidth*(x+1))+propertyEdge,\
                                        self.prop.base+self.roomheight,\
                                        self.prop.zstart+(roomsizewidth*(z+1)+propertyEdge)))

        print('rooms length is:',len(self.rooms))
                
    def addRoom(self,mc,type='basic'):
        pass
        # empty = True
        # builtrooms = []
        # for room in self.rooms:
        #     if room.full == True:
        #         empty = False
        #         builtrooms.append(room) #add the room to the builtrooms working array
        # if empty:
        #     currentRoom = self.rooms[random.randint(0,len(self.rooms)-1)] #If there are not yet any rooms select a random room as the starting room.
        #     currentRoom.createRoom(mc)
        # else:
        #     fromRoom = builtrooms[random.randint(0,len(builtrooms)-1)] #Select a room at random from the built rooms
            


class room2:
    def __init__(self,xstart,ystart,zstart,xend,yend,zend,type=0):
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xend = xend
        self.yend = yend #will normally hold room height
        self.zend = zend
        self.full = False
    def createRoom(self,mc):
        self.createBox(mc)
        self.emptyBox(mc)
        self.full = True
    def createBox(self,mc): #Creates a box of blocks used in createRoom Func
        mc.setBlocks(self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend,7)
        print('in createBox: ',self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend)
    def emptyBox(self,mc):  #Emptys the box of blocks used in createRoom

        mc.setBlocks(self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1,0)
        print('in emptyBox: ',self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1)

    def createPool(self,mc):
        pooldepth = 4
        boundrywidth = 1
        mc.setBlocks(self.xstart,self.ystart,self.zstart,\
                    self.xend,self.ystart,self.zend,24) #create outer pool shell boundry
        mc.setBlocks(self.xstart+boundrywidth,self.ystart,self.zstart+boundrywidth,\
                    self.xend-boundrywidth,self.ystart-pooldepth-1,self.zend-boundrywidth,1,2) #create pool shell
        mc.setBlocks(self.xstart+boundrywidth+1,self.ystart,self.zstart+boundrywidth+1,\
                    self.xend-boundrywidth-1,self.ystart-pooldepth,self.zend-boundrywidth-1,9) #create water




#OLD CODE

# class house:
#     def __init__(self,prop,height):
#         self.rooms = [] #every room
#         self.avaliablerooms = [] #rooms that can be built from
#         self.prop = prop #the property
#         self.height = height #the height of a room


#     def createRoomSimple(self): #start from the first room
#         if(len(self.rooms)==0): #create a room at the front
#             roomsizewidth = abs((self.prop.xstart-self.prop.xend)//3)
#             print('room width is',roomsizewidth)
#             roomsizedepth = abs((self.prop.zstart-self.prop.zend)//3)
#             print('room depth is',roomsizedepth)
#             randLoc = random.randint(0, 2)
#             newRoom = room(self.prop.xstart+(roomsizewidth*randLoc),self.prop.base,self.prop.zstart,self.prop.xstart+(roomsizewidth*(randLoc+1)),self.prop.base+self.height,self.prop.zstart+roomsizedepth)
#             self.rooms.append(newRoom)
#             self.currentRoom = newRoom
#     def createRoom(self):
#         if(len(self.rooms)==0): #if there are no rooms then create a new room at the starting location
#             #minimum size of room is 5
#             minimumroomsize = 5
#             maximumroomsize = 10
#             randStartLocX = random.randint(self.prop.xstart, self.prop.xend-minimumroomsize)
#             print('randStartLocX =',randStartLocX)
#             if(randStartLocX+maximumroomsize>self.prop.xend):
#                 randEndLocX = random.randint(randStartLocX+minimumroomsize, self.prop.xend)
#             else:
#                 randEndLocX = random.randint(randStartLocX+minimumroomsize, randStartLocX+maximumroomsize)
#             print('randEndLocX =',randEndLocX)
#             randStartLocZ = random.randint(self.prop.zstart, self.prop.zend-minimumroomsize)
#             print('randStartLocZ =',randStartLocZ)
#             if(randStartLocZ+maximumroomsize>self.prop.zend):
#                 randEndLocZ = random.randint(randStartLocZ+minimumroomsize, self.prop.zend)
#             else:
#                 randEndLocZ = random.randint(randStartLocZ+minimumroomsize, randStartLocZ+maximumroomsize)
#             print('randEndLocZ =',randEndLocZ)

#             ## create the new room
#             newRoom = room(randStartLocX,self.prop.base,randStartLocZ,randEndLocX,self.prop.base+self.height,randEndLocZ)
            
#             #created a new room, now work out its adjacencies
#             ##### This part could be added to a new function

#             if(abs(self.prop.xstart-newRoom.xstart)<minimumroomsize): #its too close to the xstart border for a new room
#                 newRoom.adjacent[0]=1
#             if(abs(self.prop.xend-newRoom.xend)<minimumroomsize): #its too close to the xend border for a new room
#                 newRoom.adjacent[1]=1
#             if(abs(self.prop.zstart-newRoom.zstart)<minimumroomsize): #its too close to the zstart border for a new room
#                 newRoom.adjacent[2]=1
#             if(abs(self.prop.zend-newRoom.zend)<minimumroomsize): #its too close to the zend border for a new room
#                 newRoom.adjacent[3]=1
#             #####

#             self.rooms.append(newRoom)
#             if(sum(newRoom.adjacent)<4):
#                 self.avaliablerooms.append(newRoom)
#             self.currentRoom = newRoom
#         else: #otherwise create a new room that connects from the previous room
#             buildFromRoom = self.avaliablerooms[random.randint(0,len(self.avaliablerooms))] #select a room at random from the list of avaliable rooms
#             #choose a wall on the buildFromRoom to create a new room from
#             newroomlocation = random.randint(0,3) #Select a random wall to draw the new room from
#             while buildFromRoom[newroomlocation] == 1: #There is already a room in that location
#                 newroomlocation = random.randint(0,3) #select another room
#             # found a location for the new room
#             print('rand int result',newroomlocation)

                

# class room:
#     def __init__(self,xstart,ystart,zstart,xend,yend,zend,adjacent=(0,0,0,0)):
#         self.xstart = xstart+1
#         self.ystart = ystart
#         self.zstart = zstart+1
#         self.xend = xend
#         self.yend = yend
#         self.zend = zend
#         self.adjacent = adjacent #xstart xend zstart zend
#     def drawRoom(self,mc):
#         mc.setBlocks(self.xstart,self.ystart,self.zstart,self.xend,self.yend,self.zend,7)
#         # change self.yend-0 to self.yend-1 to add a roof
#         # removes the middle of a room
#         mc.setBlocks(self.xstart+1,self.ystart+1,self.zstart+1,self.xend-1,self.yend-0,self.zend-1,0)