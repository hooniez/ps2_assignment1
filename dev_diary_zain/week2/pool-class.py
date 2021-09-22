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
            mc.setBlocks(self.x,self.y,self.z,self.x-6,self.y-5,self.z+10,155)#stone outline
            mc.setBlocks(self.x,self.y+1,self.z,self.x-6,self.y+1,self.z+10,85)#fences
            mc.setBlocks(self.x,self.y+1,self.z,self.x-5,self.y+1,self.z+9,0)#air
            mc.setBlocks(self.x-1,self.y,self.z+1,self.x-5,self.y-4,self.z+9,9)#water
        elif self.poolRefRight == False: # if the pool is on the back right, it will build back and to the left
            #mc.setBlocks(self.x-1,self.y,self.z,self.x-1,self.y+1,self.z,0)
            self.x +=1
            self.z +=2
            self.y -=1
            mc.setBlocks(self.x,self.y,self.z,self.x+6,self.y-5,self.z+10,155)#stone outline
            mc.setBlocks(self.x,self.y+1,self.z,self.x+6,self.y+1,self.z+10,85)#fences
            mc.setBlocks(self.x,self.y+1,self.z,self.x+6,self.y+1,self.z+9,0)#air
            mc.setBlocks(self.x+1,self.y,self.z+1,self.x+5,self.y-4,self.z+9,9)#water
        

    def findEdge(self,plotDimX,plotDimZ,mc,poolRefRight = True):#draws a lien from a corner and finds the point of intersection with the house(post house generation)
        self.startx = self.x
        self.starty = self.y
        self.startz = self.z

        self.poolRefRight = poolRefRight #determines whether it's better for the pool to be on the right or left

        self.plotDimX = plotDimX #x dimension of the plot
        self.plotDimZ = plotDimZ #z dimension of the plot
        self.z +=30 #starting the line from the back-right corner
        while mc.getBlock(self.x,self.y,self.z) == 0: # finding the point of intersection
            self.x +=1
            self.z -=1
        #mc.setBlock(self.x,self.y,self.z,1)
        self.x -=1
        self.z -=1 #providing space
        #mc.setBlock(self.x,self.y,self.z,1)

        if (mc.getBlock(self.x-8,self.y,self.z+13) == 0 and 
            mc.getBlock(self.x-8,self.y-1,self.z+13)==2):  #checking to see if the pool zone will fit
            #and mc.getBlocks(self.x,self.y,self.z,self.x - 6,self.y,self.z-10) == 0:
            #mc.setBlocks(self.x,self.y,self.z,self.x-6,self.y,self.z+10,112) # mock up pool
            #self.refBlock = self.x,self.y,self.z
            return self.poolRefRight == True
        else:
            self.poolRefRight = False # if there's no space the line will be drawn from the back left

        if self.poolRefRight == False:
            self.x = self.startx + self.plotDimX #start from back left
            self.z = self.startz + self.plotDimZ

            while mc.getBlock(self.x,self.y,self.z) == 0:#searches for intersection
                self.x -=1
                self.z -=1
                #mc.setBlock(self.x,self.y,self.z,1)

                if (mc.getBlock(self.x+8,self.y,self.z+13) == 0 and
                    mc.getBlock(self.x+8,self.y-1,self.z+13)==2):
                    #mc.setBlocks(self.x,self.y,self.z,self.x+6,self.y,self.z+10,112) #creates mock up pool
                    self.x +=1
                    #self.z -=1
                    return self.poolRefRight == False
                else:
                    pass