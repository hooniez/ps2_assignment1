class Property:
    def __init__(self,location,width,depth):
        self.xstart = location.x+1 #starts 1x square away from player, can be changed later
        self.base = location.y-1 #starts -1y square away from player
        self.zstart = location.z+1 #starts 1z square away from player
        self.xend = location.x+width+1 #extends width +1 from player in x direction
        self.zend = location.z+depth+1 #extends width +1 from player in z direction
        self.width = width #to simplify future calculations
        self.depth = depth

    def drawProperty(self,mc): #creates a property of green grass can be removed later depending on if needed.
        mc.setBlocks(self.xstart,self.base,self.zstart,self.xend,self.base,self.zend,2)