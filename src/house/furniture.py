import random

class Furniture:
    def __init__(self,startCorner,endCorner,index,allWalls): #y will hold the floor height
        self.type = 'none'
        self.color = random.randint(1, 15)
        self.index = index
        self.walls = allWalls
        self.startCorner = startCorner
        self.endCorner = endCorner

    def drawCenterTable(self,mc):
        #43
        mc,setBlocks(
                    self.startCorner['x'],
                    self.startCorner['y'],
                    self.startCorner['z'],
                    self.startCorner['x'],
                    self.startCorner['y'],
                    self.endCorner['z'],
                    )
        pass


    def createCouch(self,mc): #Couches stick to the side of the room,
        roomWidth = abs(self.startCorner['x'] - self.endCorner['x'])
        roomHeight = abs(self.startCorner['y'] - self.endCorner['y'])
        roomDepth = abs(self.startCorner['z'] - self.endCorner['z'])
        chairWidth01 = roomDepth-6
        chairWidth23 = roomWidth-6
        adjustment = [0,0,0,0] #top bot left right
        for i, wall in enumerate(self.walls):
            if wall == None:
                pass
            else:
                if wall == 'stairsUpper' or wall == 'stairsLower' or wall=='couch':
                    adjustment[i] = 2
        if self.index == 0: #on the bot side
            mc.setBlocks(
                self.startCorner['x']+1,
                self.startCorner['y']+1,
                self.startCorner['z']+2+adjustment[2],
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.endCorner['z']-2-adjustment[3],
                159,
                self.color
            )

            mc.setBlocks(
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.startCorner['z']+3+adjustment[2],
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.endCorner['z']-3-adjustment[3],
                182
            )

        if(self.index == 1):
            mc.setBlocks(
                self.endCorner['x']-2,
                self.startCorner['y']+1,
                self.startCorner['z']+2+adjustment[2],
                self.endCorner['x']-1,
                self.startCorner['y']+1,
                self.endCorner['z']-2-adjustment[3],
                159,
                self.color
            )

            mc.setBlocks(
                self.endCorner['x']-2,
                self.startCorner['y']+1,
                self.startCorner['z']+3+adjustment[2],
                self.endCorner['x']-2,
                self.startCorner['y']+1,
                self.endCorner['z']-3-adjustment[3],
                182
            )
        if(self.index == 2):
            mc.setBlocks(
                self.startCorner['x']+2+adjustment[0],
                self.startCorner['y']+1,
                self.startCorner['z']+1,
                self.endCorner['x']-2-adjustment[1],
                self.startCorner['y']+1,
                self.startCorner['z']+2,
                159,
                self.color
            )
            mc.setBlocks(
                self.startCorner['x']+3+adjustment[0],
                self.startCorner['y']+1,
                self.startCorner['z']+2,
                self.endCorner['x']-3-adjustment[1],
                self.startCorner['y']+1,
                self.startCorner['z']+2,
                182
            )
        if(self.index == 3):
            mc.setBlocks(
                self.startCorner['x']+2+adjustment[0],
                self.startCorner['y']+1,
                self.endCorner['z']-2,
                self.endCorner['x']-2-adjustment[1],
                self.startCorner['y']+1,
                self.endCorner['z']-1,
                159,
                self.color
            )
            mc.setBlocks(
                self.startCorner['x']+3+adjustment[0],
                self.startCorner['y']+1,
                self.endCorner['z']-2,
                self.endCorner['x']-3-adjustment[1],
                self.startCorner['y']+1,
                self.endCorner['z']-2,
                182
            )
