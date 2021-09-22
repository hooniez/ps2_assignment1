class Furniture:
    def __init__(self,startCorner,endCorner): #y will hold the floor height
        self.type = 'none'
        self.color = 'red'
        self.startCorner = startCorner
        self.endCorner = endCorner
    def createChair(self,mc,index):
        roomWidth = abs(self.startCorner['x'] - self.endCorner['x'])
        roomHeight = abs(self.startCorner['y'] - self.endCorner['y'])
        roomDepth = abs(self.startCorner['z'] - self.endCorner['z'])
        chairWidth01 = roomDepth-6
        chairWidth23 = roomWidth-6
        if(index == 0): #on the bot side
            mc.setBlocks(
                self.startCorner['x']+1,
                self.startCorner['y']+1,
                self.startCorner['z']+2,
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.endCorner['z']-2,
                133
            )

            mc.setBlocks(
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.startCorner['z']+3,
                self.startCorner['x']+2,
                self.startCorner['y']+1,
                self.endCorner['z']-3,
                182
            )
            # mc.setBlocks(
            #     self.startCorner['x']+2,
            #     self.startCorner['y'],
            #     self.startCorner['z']+3,
            #     self.startCorner['x']+3,
            #     self.startCorner['y']+2,
            #     self.endCorner['z']-3,
            #     0
            # )

        # if(index == 1):
        #     mc.setBlocks()
        # if(index == 2):
        #     mc.setBlocks()
        # if(index == 3):
        #     mc.setBlocks()