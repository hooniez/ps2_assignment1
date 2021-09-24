import mcpi.block as block 

class Road():
    def __init__(self, mc, origin_vector, destination_vector, direction, width):
        self.origin_vector = origin_vector
        self.destination_vector = destination_vector
        self.direction = direction
        self.width = width

    def lay_road(self, mc, section):
        if section == "row":
            if self.direction == "towards_next":
                    z = self.origin_vector.z - self.width
            else:
                    z = self.origin_vector.z + self.width
            x_to_extend = 0
            y_to_extend = 0
            # while self.origin_vector.y != self.destination_vector.y:
            if self.origin_vector.y > self.destination_vector.y:  
                while self.origin_vector.y + y_to_extend > self.destination_vector.y:
                    if self.direction == "towards_next":
                        x_to_extend += 1
                    else:
                        x_to_extend -= 1
                    y_to_extend -= 1

                    mc.setBlocks(
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z,
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend,
                        z,
                        block.GLOWSTONE_BLOCK.id
                    )

                    mc.setBlocks(
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend + 1,
                        self.origin_vector.z,
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend + 4,
                        z,
                        0
                    )
                
            
            elif self.origin_vector.y < self.destination_vector.y:
                while self.origin_vector.y + y_to_extend < self.destination_vector.y:
                    
                    if self.direction == "towards_next":
                        x_to_extend += 1
                    else:
                        x_to_extend -= 1 
                    # Ascend
                    y_to_extend += 1
                    mc.setBlocks(
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z,
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend,
                        z,
                        block.GLOWSTONE_BLOCK.id
                    )
                    mc.setBlocks(
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend + 1,
                        self.origin_vector.z,
                        self.origin_vector.x + x_to_extend,
                        self.origin_vector.y + y_to_extend + 4,
                        z,
                        0
                    )
    
            # Straight line
            mc.setBlocks(
                self.origin_vector.x + x_to_extend,
                self.destination_vector.y,
                self.origin_vector.z,
                self.destination_vector.x,
                self.destination_vector.y,
                z,
                block.GLOWSTONE_BLOCK.id
            )
            mc.setBlocks(
                self.origin_vector.x + x_to_extend,
                self.destination_vector.y + 1,
                self.origin_vector.z,
                self.destination_vector.x,
                self.destination_vector.y + 4,
                z,
                0
            )
            
            # Center line
            z_to_extend = 0
            z_to_pull = 0
            if self.direction == "towards_next":
                x_to_extend = 1
                
                if (self.origin_vector.z <= self.destination_vector.z):
                    z_to_pull = -self.width
                    z_to_extend = 1                    
                else:
                    z_to_extend = -1
                    
            else:
                x_to_extend = -1
                if (self.origin_vector.z >= self.destination_vector.z):
                    z_to_pull = self.width
                    z_to_extend = -1
                else:
                    z_to_extend = 1
                    
            mc.setBlocks(
                self.destination_vector.x + x_to_extend,
                self.destination_vector.y,
                self.origin_vector.z + z_to_pull,
                self.destination_vector.x - x_to_extend,
                self.destination_vector.y,
                self.destination_vector.z + z_to_extend,
                block.DIAMOND_BLOCK
            )
            mc.setBlocks(
                self.destination_vector.x + x_to_extend,
                self.destination_vector.y + 1,
                self.origin_vector.z + z_to_pull,
                self.destination_vector.x - x_to_extend,
                self.destination_vector.y + 4,
                self.destination_vector.z + z_to_extend,
                0
            )
                    
        elif section == 'column':
            # If there's not enough space in z-axis to cover the difference in y-axis
            if self.direction == "towards_next":
                    x = self.origin_vector.x - self.width
            else:
                    x = self.origin_vector.x + self.width
            z_to_extend = 0
            y_to_extend = 0
            if self.origin_vector.y > self.destination_vector.y:
                while self.origin_vector.y + y_to_extend > self.destination_vector.y:
                    # Descend 
                    if self.direction == "towards_next":
                        z_to_extend += 1
                    else:
                        z_to_extend -= 1
                    y_to_extend -= 1

                    mc.setBlocks(
                        self.origin_vector.x,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z + z_to_extend,
                        x,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z + z_to_extend,
                        block.GLOWSTONE_BLOCK.id
                    )
                    mc.setBlocks(
                        self.origin_vector.x,
                        self.origin_vector.y + y_to_extend + 1,
                        self.origin_vector.z + z_to_extend,
                        x,
                        self.origin_vector.y + y_to_extend + 4,
                        self.origin_vector.z + z_to_extend,
                        0
                    )
                    
            
            elif self.origin_vector.y < self.destination_vector.y:
                while self.origin_vector.y + y_to_extend < self.destination_vector.y:
                    if self.direction == "towards_next":
                        z_to_extend += 1
                    else:
                        z_to_extend -= 1 
                    # Ascend
                    y_to_extend += 1
                    mc.setBlocks(
                        self.origin_vector.x,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z + z_to_extend,
                        x,
                        self.origin_vector.y + y_to_extend,
                        self.origin_vector.z + z_to_extend,
                        block.GLOWSTONE_BLOCK.id
                    )
                    mc.setBlocks(
                        self.origin_vector.x,
                        self.origin_vector.y + y_to_extend + 1,
                        self.origin_vector.z + z_to_extend,
                        x,
                        self.origin_vector.y + y_to_extend + 4,
                        self.origin_vector.z + z_to_extend,
                        0
                    )
                    
            # Straight line
            mc.setBlocks(
                self.origin_vector.x,
                self.destination_vector.y,
                self.origin_vector.z + z_to_extend,
                x,
                self.destination_vector.y,
                self.destination_vector.z,
                block.GLOWSTONE_BLOCK.id
            )
            mc.setBlocks(
                self.origin_vector.x,
                self.destination_vector.y + 1,
                self.origin_vector.z + z_to_extend,
                x,
                self.destination_vector.y + 4,
                self.destination_vector.z,
                0
            )
            
            x_to_extend = 0
            x_to_pull = 0
            # Center line
            if self.direction == "towards_next":
                z_to_extend = 1
                if (self.origin_vector.x < self.destination_vector.x):
                    x_to_pull = -self.width                    
                    x_to_extend = 1
                else:
                    x_to_extend = -1
            else:
                z_to_extend = -1
                if (self.origin_vector.x >= self.destination_vector.x):
                    x_to_pull = self.width                    
                    x_to_extend = -1
                else:
                    x_to_extend = 1
                    
            mc.setBlocks(
                self.origin_vector.x + x_to_pull,
                self.destination_vector.y,
                self.destination_vector.z + z_to_extend,
                self.destination_vector.x + x_to_extend,
                self.destination_vector.y,
                self.destination_vector.z - z_to_extend,
                block.DIAMOND_BLOCK
            )
            mc.setBlocks(
                self.origin_vector.x + x_to_pull,
                self.destination_vector.y + 1,
                self.destination_vector.z + z_to_extend,
                self.destination_vector.x + x_to_extend,
                self.destination_vector.y + 4,
                self.destination_vector.z - z_to_extend,
                0
            )
                