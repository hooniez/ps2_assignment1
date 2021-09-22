class Furniture:
    def __init__(self,startCorner,endCorner,index,allWalls): #y will hold the floor height
        self.type = 'none'
        self.color = 'red'
        self.index = index
        self.walls = allWalls
        self.startCorner = startCorner
        self.endCorner = endCorner
    def createCouch(self,mc):
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
                if wall == 'stairsUpper' or wall == 'stairsLower':
                    adjustment[i] = 2
        if self.index == 0: #on the bot side
            mc.setBlocks(
                self.startCorner['x']+1,
                self.startCorner['y']+1,
                self.startCorner['z']+2+adjustment[2],
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.endCorner['z']-2-adjustment[3],
                133
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
                133
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
        # if(self.index == 2):
        #     mc.setBlocks(
        #         self.endCorner['x']-2,
        #         self.startCorner['y']+1,
        #         self.startCorner['z']+3,
        #         self.endCorner['x']-2,
        #         self.startCorner['y']+1,
        #         self.endCorner['z']-3,
        #         182
        #     )
        # if(self.index == 3):
        #     mc.setBlocks()