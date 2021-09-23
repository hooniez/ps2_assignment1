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
        roomWidth = abs(self.startCorner['x'] - self.endCorner['x'])
        roomHeight = abs(self.startCorner['y'] - self.endCorner['y'])
        roomDepth = abs(self.startCorner['z'] - self.endCorner['z'])
        if random.randint(0, 1) == 0:
            mc.setBlocks(
                        self.startCorner['x']+roomWidth//2-1,
                        self.startCorner['y']+1,
                        self.startCorner['z']+roomDepth//2-1,
                        self.startCorner['x']+roomWidth//2+1,
                        self.startCorner['y']+1,
                        self.startCorner['z']+roomDepth//2+1,
                        43
                        )
            mc.setBlock   (
                        self.startCorner['x']+roomWidth//2,
                        self.startCorner['y']+1,
                        self.startCorner['z']+roomDepth//2,
                        118
                        )
        else:
            mc.setBlocks(
                        self.startCorner['x']+roomWidth//2-1,
                        self.startCorner['y']+1,
                        self.startCorner['z']+roomDepth//2-1,
                        self.startCorner['x']+roomWidth//2+1,
                        self.startCorner['y']+1,
                        self.startCorner['z']+roomDepth//2+1,
                        44,
                        1	
                        )
            

    def createCouch(self,mc): #Couches stick to the side of the room,
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
