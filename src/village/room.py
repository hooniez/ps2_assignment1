from mcpi.vec3 import Vec3
from furniture import Furniture
import random
import pandas as pd
import numpy as np


# ROOM HAS A MINIMUM WALLLENGTH OF 10
class Room:
    def __init__(self,xstart,ystart,zstart,xend,yend,zend,roomPos,gridX,gridZ,roomColor):
        self.color = roomColor #choose a random color wool
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xend = xend
        self.yend = yend
        self.zend = zend
        self.roomPos = roomPos #position in the rooms Array (rooms array is a property of the floor class, holds every room on the floor)
        ## Add list of rooms that are connected bot,top,left,right
        ##
        ##              Top      
        ##           ________
        ## Left     |        |     Right
        ##        X |        |
        ##          |________|
        ##              Z
        ##              Bot
        self.connectedRooms = [None,None,None,None] #bot,top,left,right #room !self.connectedRooms[0].roomType == pool
        self.gridCoord = (gridX,gridZ)
        self.full = False #Room does not exist by default
        self.roomType = 'none'
        self.buildUpAvaliablity = False
        self.walls = [None,None,None,None] #bot,top,left,right (walls array now contains eveything that sticks to a wall, e.g stairs,chairs etc)
        
        self.x_to_center = abs(self.xstart - self.xend) // 2 
        self.z_to_center = abs(self.zstart - self.zend) // 2
        self.center_point = Vec3(
            self.xstart + self.x_to_center,
            self.ystart,
            self.zstart + self.z_to_center
        )
        self.avaialble_space = None

    def createRoom(self,mc,roomtype):
        if(roomtype=='basic'):
            self.roomType = 'basic'
            self.createBox(mc)
            self.emptyBox(mc)
            self.lightenBox(mc)
            self.full = True #There is now something in the room
            self.buildUpAvaliablity = True
        if(roomtype=='pool'):
            # Check if this pool is next to another pool.
            self.roomType = 'pool'
            self.createPool(mc)
            self.full = True #There is now something in the room
            self.buildUpAvaliablity = False

        # if(roomtype=='garden'):
        #     self.buildUpAvaliablity = False
        #     self.full = True #There is now something in the room
        #     self.roomType = 'garden'
        # if(roomtype=='roomwithcouch'):
            
            #self.create Garden

    def createBox(self,mc): #Creates a box of blocks used in createRoom Func
        mc.setBlocks(
                    self.xstart,
                    self.ystart,
                    self.zstart,
                    self.xend,
                    self.yend,
                    self.zend,
                    35,
                    self.color #Room Color Selection
                    ) 
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

    # Creates a light in the middle of the room (helps with dark rooms)
    def lightenBox(self, mc):
        center_block = 209 
        torch = 50
        

        center_point_ceiling = Vec3(
            self.center_point.x,
            self.yend - 1,
            self.center_point.z
        )
        center_point_plus_x = Vec3(
            center_point_ceiling.x + 1,
            center_point_ceiling.y,
            center_point_ceiling.z
        )
        center_point_minus_x = Vec3(
            center_point_ceiling.x - 1,
            center_point_ceiling.y,
            center_point_ceiling.z
        )
        center_point_plus_z = Vec3(
            center_point_ceiling.x,
            center_point_ceiling.y,
            center_point_ceiling.z + 1
        )
        center_point_minus_z = Vec3(
            center_point_ceiling.x,
            center_point_ceiling.y,
            center_point_ceiling.z - 1
        )
        mc.setBlock(center_point_ceiling, center_block)
        mc.setBlock(center_point_plus_x, torch)
        mc.setBlock(center_point_minus_x, torch, 2)
        mc.setBlock(center_point_plus_z, torch, 3)
        mc.setBlock(center_point_minus_z, torch, 4)
        

    def createDoor(self,mc,prevRoom):
        if(prevRoom is None): #Do nothing
            pass
        else: #Previous room exists, 
            doorTypesAll = ['fullwidthDoor','singleDoor'] #Add new door types here to insert them into random selector 
            doorTypesPool = ['singleDoor']
            randomDoorType = 'singleDoor' #Default
            if(self.roomType == 'pool') or prevRoom.roomType == 'pool':
                randomDoorType = doorTypesPool[random.randint(0,len(doorTypesPool)-1)]
            else:
                randomDoorType = doorTypesAll[random.randint(0,len(doorTypesAll)-1)]

            currentLocation = self.connectedRooms.index(prevRoom) #find index of prevRoom room in the current room connectedRooms array
            self.walls[currentLocation] = randomDoorType #Remember there is a door here

            doorLocationPrev = prevRoom.connectedRooms.index(self) #find index of current room in the prevRoom room connectedRooms array

            prevRoom.walls[doorLocationPrev] = randomDoorType #Remember there is a door here
            self.drawDoor(mc,currentLocation, randomDoorType)
    
    # Start implementation of staircase
    def createStaircase(self,mc,belowRoom,randSpace): #belowroom holds the room below
        stairWidth = 2 #these are hard coded but could be changed to be given as inputs to the function at a later date
        wallWidth = 1
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        roomHeight = abs(self.ystart-self.yend)
        #door is on bot
        if(randSpace == 0): #Correct
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xstart+1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+1,
                            belowRoom.xstart+stairWidth,
                            belowRoom.ystart+i,
                            belowRoom.zstart+roomHeight+1-i,
                            35, #wool brick type
                            self.color
                            ) #brick

                mc.setBlocks(
                            belowRoom.xstart+1,
                            belowRoom.ystart+i+1,
                            belowRoom.zstart+1,
                            belowRoom.xstart+stairWidth,
                            belowRoom.ystart+i+1,
                            belowRoom.zstart+roomHeight+1-i,
                            72
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xstart+1,
                        belowRoom.yend, #Dont change
                        belowRoom.zstart+2,
                        belowRoom.xstart+stairWidth,
                        belowRoom.yend, #Dont change
                        belowRoom.zstart+roomHeight,
                        0 #air
                        )
            mc.setBlocks(
                        belowRoom.xstart+1,
                        belowRoom.yend, #Dont change
                        belowRoom.zstart+2,
                        belowRoom.xstart+2,
                        belowRoom.yend, #Dont change
                        belowRoom.zstart+2,
                        72 #air
                        )
        #door is on top
        if(randSpace == 1): #Correct
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xend-1,
                            belowRoom.ystart+i,
                            belowRoom.zend-roomHeight+i-1,
                            belowRoom.xend-stairWidth,
                            belowRoom.ystart+i,
                            belowRoom.zend-1,
                            35, #wool brick type
                            self.color
                            ) #brick
                mc.setBlocks(
                            belowRoom.xend-1,
                            belowRoom.ystart+i+1,
                            belowRoom.zend-roomHeight+i-1,
                            belowRoom.xend-stairWidth,
                            belowRoom.ystart+i+1,
                            belowRoom.zend-1,
                            72
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xend-1,
                        belowRoom.yend,
                        belowRoom.zend-roomHeight,
                        belowRoom.xend-stairWidth,
                        belowRoom.yend,
                        belowRoom.zend-2,
                        0 #air
                        )
            mc.setBlocks(
                        belowRoom.xend-1,
                        belowRoom.yend,
                        belowRoom.zend-2,
                        belowRoom.xend-stairWidth,
                        belowRoom.yend,
                        belowRoom.zend-2,
                        72 #air
                        )
        #door is on left
        if(randSpace == 2): #Correct
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xend+i-roomHeight-1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+1,
                            belowRoom.xend-1,
                            belowRoom.ystart+i,
                            belowRoom.zstart+stairWidth,
                            35, #wool brick type
                            self.color
                            ) #brick
                mc.setBlocks(
                            belowRoom.xend+i-roomHeight-1,
                            belowRoom.ystart+i+1,
                            belowRoom.zstart+1,
                            belowRoom.xend-1,
                            belowRoom.ystart+i+1,
                            belowRoom.zstart+stairWidth,
                            72
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xend-roomHeight,
                        belowRoom.yend,
                        belowRoom.zstart+1,
                        belowRoom.xend-2,
                        belowRoom.yend,
                        belowRoom.zstart+stairWidth,
                        0
                        )
            mc.setBlocks(
                        belowRoom.xend-2,
                        belowRoom.yend,
                        belowRoom.zstart+1,
                        belowRoom.xend-2,
                        belowRoom.yend,
                        belowRoom.zstart+stairWidth,
                        72
                        )
        #door is on right
        if(randSpace == 3): #Correct
            for i in range(1,roomHeight+1):
                mc.setBlocks(
                            belowRoom.xstart+1,
                            belowRoom.ystart+i,
                            belowRoom.zend-1,
                            belowRoom.xstart+roomHeight+1-i,
                            belowRoom.ystart+i,
                            belowRoom.zend-stairWidth,
                            35, #wool brick type
                            self.color
                            ) #brick
                mc.setBlocks(
                            belowRoom.xstart+1,
                            belowRoom.ystart+i+1,
                            belowRoom.zend-1,
                            belowRoom.xstart+roomHeight+1-i,
                            belowRoom.ystart+i+1,
                            belowRoom.zend-stairWidth,
                            72
                            ) #brick
            #then create a hole in the floor
            mc.setBlocks(
                        belowRoom.xstart+2,
                        belowRoom.yend,
                        belowRoom.zend-1,
                        belowRoom.xstart+roomHeight,
                        belowRoom.yend,
                        belowRoom.zend-stairWidth,
                        0
                        )
            mc.setBlocks(
                        belowRoom.xstart+2,
                        belowRoom.yend,
                        belowRoom.zend-1,
                        belowRoom.xstart+2,
                        belowRoom.yend,
                        belowRoom.zend-2,
                        72
                        )

        belowRoom.walls[randSpace] = 'stairsLower' #Set the doors array to the new space
        self.walls[randSpace] = 'stairsUpper'
    
    
    def drawDoor(self,mc,doordirection,doortype):
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        roomHeight = abs(self.ystart-self.yend)
        doorWidth = 1 #Width of the door
        doorDepth = 1 #How far the door sticks out from the wall (this is to prevent other objects from blocking the doors entry)
        doorHeight = 3
        if doortype == 'fullwidthDoor':
            doorHeight = roomHeight - 1
            if(doordirection == 0): #door is on bot
                doorWidth = roomDepth - 1
                mc.setBlocks(
                            self.xstart-doorDepth,
                            self.ystart+1,
                            self.zstart+1,
                            self.xstart+doorDepth,
                            self.ystart+doorHeight,
                            self.zstart+doorWidth,
                            0
                            )
            if(doordirection == 1): #door is on top
                doorWidth = roomDepth - 1
                mc.setBlocks(
                            self.xend+doorDepth,
                            self.ystart+1,
                            self.zstart+1,
                            self.xend-doorDepth,
                            self.ystart+doorHeight,
                            self.zstart+doorWidth,
                            0
                            )
            if(doordirection == 2): #door is on left
                doorWidth = roomWidth - 1
                mc.setBlocks(
                            self.xstart+1,
                            self.ystart+1,
                            self.zstart-doorDepth,
                            self.xstart+doorWidth,
                            self.ystart+doorHeight,
                            self.zstart+doorDepth,
                            0
                            )
            if(doordirection == 3): #door is on right]
                doorWidth = roomWidth - 1
                mc.setBlocks(
                            self.xstart+1,
                            self.ystart+1,
                            self.zend-doorDepth,
                            self.xstart+doorWidth,
                            self.ystart+doorHeight,
                            self.zend+doorDepth,
                            0
                            )
        if doortype == 'singleDoor':
            doorWidth = 1
            doorHeight = 3
            if(doordirection == 0): #door is on bot
                mc.setBlock(self.xstart,self.ystart+2,self.zstart+roomDepth//2, 64,9) #64,9)
                mc.setBlock(self.xstart,self.ystart+1,self.zstart+roomDepth//2, 64,1) #64,1)
                mc.setBlock(self.xstart,self.ystart+2,self.zstart+roomDepth//2+1, 64,12)
                mc.setBlock(self.xstart,self.ystart+1,self.zstart+roomDepth//2+1, 64,4)

            if(doordirection == 1): #door is on top
                mc.setBlock(self.xend,self.ystart+2,self.zstart+roomDepth//2, 64,9) #64,9)
                mc.setBlock(self.xend,self.ystart+1,self.zstart+roomDepth//2, 64,1) #64,1)
                mc.setBlock(self.xend,self.ystart+2,self.zstart+roomDepth//2+1, 64,12)
                mc.setBlock(self.xend,self.ystart+1,self.zstart+roomDepth//2+1, 64,4)

            if(doordirection == 2): #door is on left
                mc.setBlock(self.xstart+roomWidth//2, self.ystart+2, self.zstart, 64, 8)
                mc.setBlock(self.xstart+roomWidth//2, self.ystart+1, self.zstart, 64, 0)
                mc.setBlock(self.xstart+roomWidth//2+1, self.ystart+2, self.zstart, 64, 15)
                mc.setBlock(self.xstart+roomWidth//2+1, self.ystart+1, self.zstart, 64, 7)

            if(doordirection == 3): #door is on right
                mc.setBlock(self.xstart+roomWidth//2, self.ystart+2, self.zend, 64, 8)
                mc.setBlock(self.xstart+roomWidth//2, self.ystart+1, self.zend, 64, 0)
                mc.setBlock(self.xstart+roomWidth//2+1, self.ystart+2, self.zend, 64, 15)
                mc.setBlock(self.xstart+roomWidth//2+1, self.ystart+1, self.zend, 64, 7)

    def createRoof(self,mc, adjustmentsArray,overlapArray):
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        for i in range(0,roomDepth//2,1):
            mc.setBlocks(
                        self.xstart+i+adjustmentsArray[0]-overlapArray[0],
                        self.yend,
                        self.zstart+adjustmentsArray[2]+i-overlapArray[2],
                        self.xend-i-adjustmentsArray[1]+overlapArray[1],
                        self.yend+i,
                        self.zend-adjustmentsArray[3]-i+overlapArray[3],
                        45
                        )    

    # MUST IMPLEMENT CHANGES TO PREVENT POOL CREATION ON ANYTHING OTHER THAN GROUND LEVEL
    def createPool(self, mc):
        pooldepth = 4
        boundrywidth = 2
        #First create the basic pool
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
        #Now connect to nearby pools:
        mc.setBlocks(
                    self.xstart+boundrywidth,
                    self.ystart+1,
                    self.zstart+boundrywidth,
                    self.xend-boundrywidth,
                    self.ystart+1,
                    self.zend-boundrywidth,
                    85
                    )#creates fences above granite outline layer
        mc.setBlocks(
                    self.xstart+boundrywidth+1,
                    self.ystart+1,
                    self.zstart+boundrywidth+1,
                    self.xend-boundrywidth-1,
                    self.ystart+1,
                    self.zend-boundrywidth-1,
                    0
                    )#hollows out the fences created
 

    def createPoolConnections(self, mc):
        pooldepth = 4
        boundrywidth = 2
        for index, conRoom in enumerate(self.connectedRooms):
            if conRoom == None: #Do nothing
                pass
            else:
                if conRoom.roomType == 'pool':
                    #set the walls array
                    self.walls[index] = 'poolJoin'
                    if(index) == 0: #Its on the bot side
                        conRoom.walls[1] = 'poolJoin'
                        mc.setBlocks(
                                    conRoom.xend-1, #fixed
                                    self.ystart, #fixed
                                    self.zstart+boundrywidth,
                                    self.xstart+1,
                                    self.ystart-pooldepth-1, #fixed
                                    self.zend-boundrywidth,
                                    1,
                                    2
                                    ) #create pool shell
                        mc.setBlocks(
                                    conRoom.xend-1, #fixed
                                    self.ystart+1, #fixed
                                    self.zstart+boundrywidth,
                                    self.xstart+1,
                                    self.ystart+1, #fixed
                                    self.zend-boundrywidth,
                                    85
                                    )#creates fences
                        mc.setBlocks(
                                    conRoom.xend-boundrywidth, #fixed
                                    self.ystart+1, #fixed
                                    self.zstart+boundrywidth+1,
                                    self.xstart+boundrywidth,
                                    self.ystart+1, #fixed
                                    self.zend-boundrywidth-1,
                                    0
                                    )#hollows fence                                       
                        mc.setBlocks(
                                    conRoom.xend-boundrywidth, #fixed
                                    self.ystart, #fixed
                                    self.zstart+boundrywidth+1,
                                    self.xstart+boundrywidth,
                                    self.ystart-pooldepth, #fixed
                                    self.zend-boundrywidth-1,
                                    9
                                    ) #create pool shell


                    if(index) == 1: #It's on the top side
                        conRoom.walls[0] = 'poolJoin'
                        mc.setBlocks(
                                    self.xend-1, #fixed
                                    self.ystart, #fixed
                                    self.zstart+boundrywidth,
                                    conRoom.xstart+1,
                                    self.ystart-pooldepth-1, #fixed
                                    self.zend-boundrywidth,
                                    1,
                                    2
                                    ) #create pool shell
                        mc.setBlocks(
                                    self.xend-1, #fixed
                                    self.ystart+1, #fixed
                                    self.zstart+boundrywidth,
                                    conRoom.xstart+1,
                                    self.ystart+1, #fixed
                                    self.zend-boundrywidth,
                                    85
                                    )#creates fences
                        mc.setBlocks(
                                    self.xend-boundrywidth, #fixed
                                    self.ystart+1, #fixed
                                    self.zstart+boundrywidth+1,
                                    conRoom.xstart+boundrywidth,
                                    self.ystart+1, #fixed
                                    self.zend-boundrywidth-1,
                                    0
                                    )#hollows fence                                    
                        mc.setBlocks(
                                    self.xend-boundrywidth, #fixed
                                    self.ystart, #fixed
                                    self.zstart+boundrywidth+1,
                                    conRoom.xstart+boundrywidth,
                                    self.ystart-pooldepth, #fixed
                                    self.zend-boundrywidth-1,
                                    9
                                    ) #create pool shell

                    if(index) == 2: #It's on the left side
                        conRoom.walls[3] = 'poolJoin'
                        mc.setBlocks(
                                    self.xstart+boundrywidth, #fixed
                                    self.ystart, #fixed
                                    conRoom.zend-1,
                                    self.xend-boundrywidth,
                                    self.ystart-pooldepth-1, #fixed
                                    self.zstart+1,
                                    1,
                                    2
                                    ) #create pool shell
                        mc.setBlocks(
                                    self.xstart+boundrywidth, #fixed
                                    self.ystart+1, #fixed
                                    conRoom.zend-1,
                                    self.xend-boundrywidth,
                                    self.ystart+1, #fixed
                                    self.zstart+1,
                                    85
                                    )#creates fences
                        mc.setBlocks(
                                    self.xstart+boundrywidth+1, #fixed
                                    self.ystart+1, #fixed
                                    conRoom.zend-boundrywidth,
                                    self.xend-boundrywidth-1,
                                    self.ystart+1, #fixed
                                    self.zstart+boundrywidth,
                                    0
                                    )#hollows fence   
                        mc.setBlocks(
                                    self.xstart+boundrywidth+1, #fixed
                                    self.ystart, #fixed
                                    conRoom.zend-boundrywidth,
                                    self.xend-boundrywidth-1,
                                    self.ystart-pooldepth, #fixed
                                    self.zstart+boundrywidth,
                                    9
                                    ) #create pool shell

                    if(index) == 3: #It's on the right side
                        conRoom.walls[2] = 'poolJoin'
                        mc.setBlocks(
                                    self.xstart+boundrywidth, #fixed
                                    self.ystart, #fixed
                                    self.zend-1,
                                    self.xend-boundrywidth,
                                    self.ystart-pooldepth-1, #fixed
                                    conRoom.zstart+1,
                                    1,
                                    2
                                    ) #create pool shell
                        mc.setBlocks(
                                    self.xstart+boundrywidth, #fixed
                                    self.ystart+1, #fixed
                                    self.zend-1,
                                    self.xend-boundrywidth,
                                    self.ystart+1, #fixed
                                    conRoom.zstart+1,
                                    85
                                    )#creates fences
                        mc.setBlocks(
                                    self.xstart+boundrywidth+1, #fixed
                                    self.ystart+1, #fixed
                                    self.zend-1,
                                    self.xend-boundrywidth-1,
                                    self.ystart+1, #fixed
                                    conRoom.zstart+boundrywidth,
                                    9
                                    )#hollows fence                                                                           
                        mc.setBlocks(
                                    self.xstart+boundrywidth+1, #fixed
                                    self.ystart, #fixed
                                    self.zend-1,
                                    self.xend-boundrywidth-1,
                                    self.ystart-pooldepth, #fixed
                                    conRoom.zstart+boundrywidth,
                                    9
                                    ) #create pool shell


    def calsAddfurn(self,mc):
        #look for a spair wall space
        #draw a piece of furniture there
        startCorner = {'x':self.xstart,'y':self.ystart,'z':self.zstart}
        endCorner = {'x':self.xend,'y':self.yend,'z':self.zend}
        print('walls array is',self.walls)
        if self.roomType == 'pool': #don't draw if its a pool
            return
        for index,space in enumerate(self.walls):
            Furniture(startCorner, endCorner, index, self.walls).createCarpet(mc)
            if space == None: # its empty
                #create a piece of furniture
                if random.randint(0, 2) <= 1:
                    furn = Furniture(startCorner,endCorner,index,self.walls).createCouch(mc)
                    self.walls[index] = 'couch'
                else:
                    furn = Furniture(startCorner,endCorner,index,self.walls).createDesk(mc)
                    self.walls[index] = 'desk'
        Furniture(startCorner,endCorner,index,self.walls).createCenterTable(mc)


    def findStairSpaceOnRoomWalls(self,belowRoom):
        #Check if the below room has space for a staircase:
        belowSpace = belowRoom.walls #get the location of walls
        currentSpace = self.walls #get the location of walls
        avaliableSpace = []
        for i in range(len(currentSpace)):
            if (currentSpace[i] == None) and (belowSpace[i] == None): #this slot is avaliable
                avaliableSpace.append(i)
        return avaliableSpace

    def createWindow(self,mc,windowLoc):
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

    def scanRoom(self, mc):
        space_above_floor = np.array(list(mc.getBlocks(
            self.xstart + 1,
            self.ystart + 1,
            self.zstart + 1,
            self.xend - 1,
            self.ystart + 1,
            self.zend - 1
        )))

        space_of_the_floor = np.array(list(mc.getBlocks(
            self.xstart + 1,
            self.ystart,
            self.zstart + 1,
            self.xend - 1,
            self.ystart,
            self.zend - 1
        )))

        idx = pd.MultiIndex.from_product([np.arange(self.xstart + 1, self.xend), np.arange(self.zstart + 1, self.zend)])
        idx.set_names(['x', 'z'], inplace=True)

        space_above_floor_boolean = space_above_floor == 0
        space_of_the_floor_boolean = space_of_the_floor != 0
        space_boolean = np.minimum(space_above_floor_boolean, space_of_the_floor_boolean)
        
        if np.all(space_boolean):
            pass
        else:
            self.furnishRoomWithStairs(mc, idx, space_boolean)
    
    def furnishRoomWithStairs(self, mc, idx, space_boolean):
        randomSingleBlocks = np.array([91, 92, 118, 117, 116, 154, 218, 63, 145, 146, 84, 58, 54, 25])
        

        df = pd.DataFrame({'available space': space_boolean}, index=idx)
    
        df = df[df['available space'] == True]

        for idx, df_select in df.groupby(level=[0, 1]):
            randnum = np.random.randint(0, 11)
            if randnum == 3:
                randomBlock = np.random.choice(randomSingleBlocks)
                mc.setBlock(idx[0], self.ystart + 1, idx[1], randomBlock)

            else:
                mc.setBlock(idx[0], self.ystart + 1, idx[1], 171)
            

        df = df.unstack(level=1)
        # print(df)
        # print(df.isna().sum())