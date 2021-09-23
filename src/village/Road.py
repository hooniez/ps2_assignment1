import mcpi.block as block 

class Road():
    def __init__(self, mc, origin_point, destination_point, direction):
        self.origin_point = origin_point
        self.destination_point = destination_point
        self.direction = direction

    def lay_road(self, mc, slot):

        if slot == "row":
            if abs(self.origin_point.x - self.destination_point.x) <= abs(self.origin_point.y - self.destination_point.y):
                return
            else:

                road_width = 3
                if self.direction == "towards_next":
                        z = self.origin_point.z - road_width
                else:
                        z = self.origin_point.z + road_width
                x_to_extend = 0
                y_to_extend = 0
                # while self.origin_point.y != self.destination_point.y:
                if self.origin_point.y > self.destination_point.y:
                    
                    
                    while self.origin_point.y + y_to_extend > self.destination_point.y:
                        if self.direction == "towards_next":
                            x_to_extend += 1
                        else:
                            x_to_extend -= 1

                        y_to_extend -= 1
    
                        mc.setBlocks(
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z,
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend,
                            z,
                            block.GLOWSTONE_BLOCK.id
                        )
    
                        mc.setBlocks(
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend + 1,
                            self.origin_point.z,
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend + 5,
                            z,
                            0
                        )
                    
                
                elif self.origin_point.y < self.destination_point.y:
                    while self.origin_point.y + y_to_extend < self.destination_point.y:
                        
                        if self.direction == "towards_next":
                            x_to_extend += 1
                        else:
                            x_to_extend -= 1 
                        # Ascend
                        y_to_extend += 1
                        mc.setBlocks(
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z,
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend,
                            z,
                            block.GLOWSTONE_BLOCK.id
                        )
                        mc.setBlocks(
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend + 1,
                            self.origin_point.z,
                            self.origin_point.x + x_to_extend,
                            self.origin_point.y + y_to_extend + 5,
                            z,
                            0
                        )
        
                # Straight line
                mc.setBlocks(
                    self.origin_point.x + x_to_extend,
                    self.destination_point.y,
                    self.origin_point.z,
                    self.destination_point.x,
                    self.destination_point.y,
                    z,
                    block.GLOWSTONE_BLOCK.id
                )
                mc.setBlocks(
                    self.origin_point.x + x_to_extend,
                    self.destination_point.y + 1,
                    self.origin_point.z,
                    self.destination_point.x,
                    self.destination_point.y + 5,
                    z,
                    0
                )
                
                # Center line
    
                if self.direction == "towards_next":
                    x_to_extend = 1  
                else:
                    x_to_extend = -1

                z_to_extend = 0
                if (self.origin_point.z < self.destination_point.z) & (self.direction == 'towards_next'):
                    z_to_extend = -(road_width)
                if (self.origin_point.z > self.destination_point.z) & (self.direction == 'towards_previous'):
                    z_to_extend = road_width
                        
                mc.setBlocks(
                    self.destination_point.x + x_to_extend,
                    self.destination_point.y,
                    self.origin_point.z + z_to_extend,
                    self.destination_point.x - x_to_extend,
                    self.destination_point.y,
                    self.destination_point.z,
                    block.GLOWSTONE_BLOCK
                )
                mc.setBlocks(
                    self.destination_point.x + x_to_extend,
                    self.destination_point.y + 1,
                    self.origin_point.z + z_to_extend,
                    self.destination_point.x - x_to_extend,
                    self.destination_point.y + 5,
                    self.destination_point.z,
                    0
                )

        elif slot == 'column':
            
            if abs(self.origin_point.z - self.destination_point.z) <= abs(self.origin_point.y - self.destination_point.y):
                pass
            else:

                road_width = 3
                if self.direction == "towards_next":
                        x = self.origin_point.x - road_width
                else:
                        x = self.origin_point.x + road_width
                z_to_extend = 0
                y_to_extend = 0
                # while self.origin_point.y != self.destination_point.y:
                if self.origin_point.y > self.destination_point.y:
                    while self.origin_point.y + y_to_extend > self.destination_point.y:
                        if self.direction == "towards_next":
                            z_to_extend += 1
                        else:
                            z_to_extend -= 1
                        
    
                        # Descend

                        y_to_extend -= 1
    
                        mc.setBlocks(
                            self.origin_point.x,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z + z_to_extend,
                            x,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z + z_to_extend,
                            block.GLOWSTONE_BLOCK.id
                        )
    
                        mc.setBlocks(
                            self.origin_point.x,
                            self.origin_point.y + y_to_extend + 1,
                            self.origin_point.z + z_to_extend,
                            x,
                            self.origin_point.y + y_to_extend + 5,
                            self.origin_point.z + z_to_extend,
                            0
                        )
                        
                
                elif self.origin_point.y < self.destination_point.y:
                    while self.origin_point.y + y_to_extend < self.destination_point.y:
                        
                        if self.direction == "towards_next":
                            z_to_extend += 1
                        else:
                            z_to_extend -= 1 
                        # Ascend
                        y_to_extend += 1
                        mc.setBlocks(
                            self.origin_point.x,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z + z_to_extend,
                            x,
                            self.origin_point.y + y_to_extend,
                            self.origin_point.z + z_to_extend,
                            block.GLOWSTONE_BLOCK.id
                        )
                        mc.setBlocks(
                            self.origin_point.x,
                            self.origin_point.y + y_to_extend + 1,
                            self.origin_point.z + z_to_extend,
                            x,
                            self.origin_point.y + y_to_extend + 5,
                            self.origin_point.z + z_to_extend,
                            0
                        )
                        
                    
                    
    
                # Straight line
                mc.setBlocks(
                    self.origin_point.x,
                    self.destination_point.y,
                    self.origin_point.z + z_to_extend,
                    x,
                    self.destination_point.y,
                    self.destination_point.z,
                    block.GLOWSTONE_BLOCK.id
                )
                mc.setBlocks(
                    self.origin_point.x,
                    self.destination_point.y + 1,
                    self.origin_point.z + z_to_extend,
                    x,
                    self.destination_point.y + 5,
                    self.destination_point.z,
                    0
                )


                
                # Center line
                
    
                if self.direction == "towards_next":
                    z_to_extend = 1
                    x_to_extend = road_width

                else:
                    z_to_extend = -1
                    x_to_extend = -(road_width)
                        

                mc.setBlocks(
                    x + x_to_extend,
                    self.destination_point.y,
                    self.destination_point.z + z_to_extend,
                    self.destination_point.x,
                    self.destination_point.y,
                    self.destination_point.z - z_to_extend,
                    block.GLOWSTONE_BLOCK
                )

                
                mc.setBlocks(
                    x + x_to_extend,
                    self.destination_point.y + 1,
                    self.destination_point.z + z_to_extend,
                    self.destination_point.x,
                    self.destination_point.y + 5,
                    self.destination_point.z - z_to_extend,
                    0
                )
