from mcpi.minecraft import Minecraft
import random
import numpy as np
import mcpi.block as block 
from mcpi.vec3 import Vec3

''' 
    Let's get some terminology out of the way. 
    Width refers to the number of blocks in x-axis
    Length refers to the number of blocks in z-axis
    When width is used instead of length for z value, it will be suffixed with z. (e.g. width_z)
'''

mc = Minecraft.create()

def clear_the_foundation(start_vector, end_vector):
        mc.setBlocks(start_vector.x, start_vector.y + 1, start_vector.z, end_vector.x, end_vector.y + 100 , end_vector.z, 0)
        
def lay_foundation(start_vector, end_vector, building_block):
    mc.setBlocks(start_vector, end_vector, building_block)
    clear_the_foundation(start_vector, end_vector)

def get_height_actual_block(x, z):
    ''' Ensure blocks like LEAVES are excluded from the method mc.getHeight'''
    blocks_to_avoid = [block.LEAVES.id]
    height = mc.getHeight(x,z)
    random_block = mc.getBlock(x, height, z)
    while random_block in blocks_to_avoid:
        height -= 1
        random_block = mc.getBlock(x, height, z)
    return height



class Village():
    def __init__(self, mc, width_x, width_z):
        ''' Cells generated from num_rows and num_columns make empty plots into which foundations can be generated one per each '''
        self.foundation_size_max = 20
        self.buffer_x_min = self.foundation_size_max // 5
        self.buffer_x_max = 3 * self.buffer_x_min
        self.buffer_z_min = 0
        self.buffer_z_max = self.foundation_size_max

        self.foundation_wrappers = [] 
        self.foundation_width_spaces_between = []
        self.foundation_length_spaces_between = []
        self.foundation_longest_lengths = [0]

        self.player_pos = mc.player.getTilePos()
        self.width_z = width_z 
        self.width_x = width_x

    
    def random_grid_calculator(self):
        ''' Randomly assigns space to a grid for foundations and buffers '''
        row = 0
        remaining_width = self.width_x 
        remaining_length = self.width_z
        foundation_wrapper_max_width = self.foundation_size_max + (2 * self.buffer_x_max)
        foundation_wrapper_max_length = self.foundation_size_max + self.buffer_z_max
        while remaining_length >= foundation_wrapper_max_length:
            longest_length = 0
            self.foundation_wrappers.append([])
            self.foundation_width_spaces_between.append([])
            remaining_width = self.width_x 
            while remaining_width >= foundation_wrapper_max_width:
                foundation_wrapper = Foundation_wrapper(self.buffer_x_min, self.buffer_x_max, self.buffer_z_min, self.buffer_z_max, self.foundation_size_max)
                if foundation_wrapper.length > longest_length:
                    longest_length = foundation_wrapper.length
                self.foundation_wrappers[row].append(foundation_wrapper)
                self.foundation_width_spaces_between[row].append(0)
                remaining_width -= foundation_wrapper.width
            else:
                self.foundation_longest_lengths.append(longest_length)
                self.foundation_width_spaces_between[row].pop()
                
            num_spaces = len(self.foundation_width_spaces_between[row])

            if num_spaces > 0:
                while remaining_width != 0:
                    random_space_slot = random.randint(0, num_spaces - 1)
                    random_space = random.randint(0, remaining_width)
                    remaining_width -= random_space
                    self.foundation_width_spaces_between[row][random_space_slot] += random_space

            self.foundation_length_spaces_between.append(0)
            row += 1
            remaining_length -= longest_length

        else:
            self.foundation_length_spaces_between.pop()
            num_spaces = len(self.foundation_length_spaces_between)

            if num_spaces > 0:
                while remaining_length != 0:
                    random_space_slot = random.randint(0, num_spaces - 1)
                    random_space = random.randint(0, remaining_length)
                    remaining_length -= random_space
                    self.foundation_length_spaces_between[random_space_slot] += random_space

    def visualise_grid(self, current_x, current_z, foundation_wrapper):
        # foundation_conatiner
        lay_foundation(Vec3(current_x + foundation_wrapper.buffer_right_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.BRICK_BLOCK.id)
        # buffer_right
        lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), 
        Vec3(current_x + foundation_wrapper.buffer_right_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.WOOL.id)
        # buffer_left
        lay_foundation(Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length),
         Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.WOOL.id)
        #buffer_bootm                
        lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z), current_z), Vec3(current_x + foundation_wrapper.buffer_bottom_width, get_height_actual_block(current_x + foundation_wrapper.buffer_bottom_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), block.DIAMOND_BLOCK)
        #buffer_top
        lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
         Vec3(current_x + foundation_wrapper.width, get_height_actual_block(current_x + foundation_wrapper.width, current_z + foundation_wrapper.length), current_z + foundation_wrapper.length), block.LAPIS_LAZULI_BLOCK)

    
    def foundation_generator(self):
        ''' After calculating where to place foundations with random_grid_calculator(), set blocks in Mincraft '''
        self.random_grid_calculator()
        
        current_z = self.player_pos.z + 1
        for idx_r, row in enumerate(self.foundation_wrappers):
            current_x = self.player_pos.x + 1
            current_z += self.foundation_longest_lengths[idx_r] + 1
            for idx_f, foundation_wrapper in enumerate(row):
                x = current_x + foundation_wrapper.buffer_right_width + 1
                z = current_z + foundation_wrapper.buffer_bottom_length + 1
                y = mc.getHeight(x,z)
                foundation = Foundation(x, y, z)
                foundation_wrapper.foundation = foundation

                self.visualise_grid(current_x, current_z, foundation_wrapper)

                foundation.lay_foundation()
                
                if idx_f != len(row) - 1:
                    current_x += (foundation_wrapper.width + self.foundation_width_spaces_between[idx_r][idx_f] + 1)

    def road_generator(self, direction):
        if direction == "row":
            for row in self.foundation_wrappers:
                for idx, current_foundation_wrapper in enumerate(row):
                    current_foundation = current_foundation_wrapper.foundation
    
                    if idx == len(row) - 1:
                        previous_foundation_wrapper = row[idx - 1]
                        previous_foundation = previous_foundation_wrapper.foundation 
                        
                        road_mid_point_between_current_and_previous = Vec3(
                            (current_foundation.start_vector.x + previous_foundation.end_vector.x) // 2,
                            (current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2,
                            (current_foundation.start_vector.z + previous_foundation.end_vector.z) // 2
                        )
    
                        road = Road(mc, current_foundation.start_vector, road_mid_point_between_current_and_previous, "towards_previous")
                        road.test(mc, direction)
                        print(f"INDEX IS {idx}, for this foundation mid point's CURRENT_AND_PREVIOUS y value is: {(current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2}")
                    elif idx == 0:
                        next_foundation_wrapper = row[idx+ 1]
                        next_foundation = next_foundation_wrapper.foundation
                        road_mid_point_between_current_and_next = Vec3(
                            (current_foundation.end_vector.x + next_foundation.start_vector.x) // 2,
                            (current_foundation.end_vector.y + next_foundation.start_vector.y) // 2,
                            (current_foundation.end_vector.z + next_foundation.start_vector.z) // 2
                        )

                        
                        road = Road(mc, current_foundation.end_vector, road_mid_point_between_current_and_next, "towards_next")
                        road.test(mc, direction)
                        print(f"INDEX IS {idx}, for this foundation mid point's CURRENT_AND_NEXT y value is: {(current_foundation.end_vector.y + next_foundation.start_vector.y) // 2}")
                    else:
                        # The first foundation in a row
                        previous_foundation_wrapper = row[idx - 1]
                        next_foundation_wrapper = row[idx+ 1]
    
                        previous_foundation = previous_foundation_wrapper.foundation 
                        next_foundation = next_foundation_wrapper.foundation
                        
                        
                        # The destination point should be a mid point between foundations
                        road_mid_point_between_current_and_previous = Vec3(
                            (current_foundation.start_vector.x + previous_foundation.end_vector.x) // 2,
                            (current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2,
                            (current_foundation.start_vector.z + previous_foundation.end_vector.z) // 2
                        )
        
                        road_mid_point_between_current_and_next = Vec3(
                            (current_foundation.end_vector.x + next_foundation.start_vector.x) // 2,
                            (current_foundation.end_vector.y + next_foundation.start_vector.y) // 2,
                            (current_foundation.end_vector.z + next_foundation.start_vector.z) // 2
                        )

                        
                        print(f"INDEX IS {idx}, for this foundation mid point's CURRENT_AND_PREVIOUS y value is: {(current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2}")
                        print(f"INDEX IS {idx}, for this foundation mid point's CURRENT_AND_NEXT y value is: {(current_foundation.end_vector.y + next_foundation.start_vector.y) // 2}")

        
    
                        road = Road(mc, current_foundation.start_vector, road_mid_point_between_current_and_previous, "towards_previous")
                        road.test(mc, direction)
                        
                        road = Road(mc, current_foundation.end_vector, road_mid_point_between_current_and_next, "towards_next")
                        road.test(mc, direction)

                print("-" * 15)

        elif direction == 'column':
            # Make sure all rows have the same number of foundations
            max_foundations = len(self.foundation_wrappers[0])
            for row in self.foundation_wrappers:
                if max_foundations < len(row):
                    max_foundations = len(row)
            for row in self.foundation_wrappers:
                while len(row) < max_foundations:
                    row.append(None)

            np_foundation_wrappers = np.array(self.foundation_wrappers, dtype='object')
            foundation_wrappers = np_foundation_wrappers.T.tolist()

            for column in foundation_wrappers:
                for idx, current_foundation_wrapper in enumerate(column):
                    if current_foundation_wrapper == None:
                        pass
                    else:
                        current_foundation = current_foundation_wrapper.foundation
        
                        if idx == len(column) - 1:
                            if column[idx- 1] != None:
                                previous_foundation_wrapper = column[idx - 1]
                                previous_foundation = previous_foundation_wrapper.foundation 
                                
                                road_mid_point_between_current_and_previous = Vec3(
                                    (current_foundation.start_vector.x + previous_foundation.end_vector.x) // 2,
                                    (current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2,
                                    (current_foundation.start_vector.z + previous_foundation.end_vector.z) // 2
                                )
            
                                road = Road(mc, current_foundation.start_vector, road_mid_point_between_current_and_previous, "towards_previous")
                                road.test(mc, direction)
                        
                        elif idx == 0:
                            if column[idx+ 1] != None:
                                next_foundation_wrapper = column[idx+ 1]
                                next_foundation = next_foundation_wrapper.foundation
                                road_mid_point_between_current_and_next = Vec3(
                                    (current_foundation.end_vector.x + next_foundation.start_vector.x) // 2,
                                    (current_foundation.end_vector.y + next_foundation.start_vector.y) // 2,
                                    (current_foundation.end_vector.z + next_foundation.start_vector.z) // 2
                                )
        
                                
                                road = Road(mc, current_foundation.end_vector, road_mid_point_between_current_and_next, "towards_next")
                                road.test(mc, direction)
                        else:
                            # The first foundation in a row
                            if column[idx- 1] != None:
                                previous_foundation_wrapper = column[idx - 1]
                                previous_foundation = previous_foundation_wrapper.foundation 
                                # The destination point should be a mid point between foundations
                                road_mid_point_between_current_and_previous = Vec3(
                                    (current_foundation.start_vector.x + previous_foundation.end_vector.x) // 2,
                                    (current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2,
                                    (current_foundation.start_vector.z + previous_foundation.end_vector.z) // 2
                                )
    
                                road = Road(mc, current_foundation.start_vector, road_mid_point_between_current_and_previous, "towards_previous")
                                road.test(mc, direction)

                            if column[idx+ 1] != None:
                                next_foundation_wrapper = column[idx+ 1]
                                next_foundation = next_foundation_wrapper.foundation
                                road_mid_point_between_current_and_next = Vec3(
                                    (current_foundation.end_vector.x + next_foundation.start_vector.x) // 2,
                                    (current_foundation.end_vector.y + next_foundation.start_vector.y) // 2,
                                    (current_foundation.end_vector.z + next_foundation.start_vector.z) // 2
                                )
                                road = Road(mc, current_foundation.end_vector, road_mid_point_between_current_and_next, "towards_next")
                                road.test(mc, direction)

                            
        
                            
                            
                            
                            
                            
            
                            
    
                            
                            
    
            
        
                            
                            
                            
    

    


            

                

                
                    
                     

            


                
                     









class Foundation():
    # half the blocks > AIR = Stop layering
    def __init__(self, x, y, z):
        self.width_x = random.randrange(8, 20, 2) 
        self.width_z = random.randrange(8, 20, 2) 
        # vectors stores random vector and west, northwest, north relative to the random vector
        self.vectors = {'southeast': Vec3(x, get_height_actual_block(x,z), z), 'southwest': Vec3(x + self.width_x, get_height_actual_block(x + self.width_x ,z), z), 'northwest': Vec3(x + self.width_x, get_height_actual_block(x + self.width_x, z + self.width_z), z + self.width_z), 'northeast': Vec3(x, get_height_actual_block(x, z + self.width_z), z + self.width_z)}
        self.start_vector = None
        self.end_vector = None
        self.center_vector = None
        self.highest_vector = None
        self.building_block = block.GLOWSTONE_BLOCK.id
    
    def position_vectors(self):
        ''' Find the vector with the highest y-axis and set every vector's height to it 
            Assign start_vector, end_vector, and center_vector with values.
        '''
    
        highest_vector_val = self.vectors['southeast'].y    
        for key, vec in self.vectors.items():
            vector_val = vec.y
            if  vector_val > highest_vector_val:
                highest_vector_val = vector_val
                self.highest_vector = vec

        # Set each height to the highest height
        for vector in self.vectors.values():
            vector.y = highest_vector_val

        self.start_vector = self.vectors['southeast']
        self.end_vector = self.vectors['northwest']
        self.center_vector = Vec3((self.start_vector.x + self.end_vector.x) / 2, self.start_vector.y, (self.start_vector.z + self.end_vector.z) / 2)


    def clear_the_foundation(self):
        mc.setBlocks(self.start_vector.x, self.start_vector.y + 1, self.start_vector.z, self.end_vector.x, self.end_vector.y + 100 , self.end_vector.z, 0)
        
    def lay_foundation(self):
        self.position_vectors()
        mc.setBlocks(self.start_vector, self.end_vector, self.building_block)
        
        for vec in self.vectors.values():
            mc.setBlocks(vec.x, vec.y - 1, vec.z, vec.x, vec.y - 150, vec.z, self.building_block)

        self.clear_the_foundation()

class Road():
    def __init__(self, mc, origin_point, destination_point, direction):
        self.origin_point = origin_point
        self.destination_point = destination_point
        self.direction = direction

    def test(self, mc, slot):



        if slot == "row":
            if abs(self.origin_point.x - self.destination_point.x) < abs(self.origin_point.y - self.destination_point.y):
                pass
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
                            self.origin_point.y + y_to_extend + 20,
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
                            self.origin_point.y + y_to_extend + 20,
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
                    block.COBBLESTONE.id
                )
                mc.setBlocks(
                    self.origin_point.x + x_to_extend,
                    self.destination_point.y + 1,
                    self.origin_point.z,
                    self.destination_point.x,
                    self.destination_point.y + 20,
                    z,
                    0
                )
                
                # Center line
    
                if self.direction == "towards_next":
                    x_to_extend = 1  
                else:
                    x_to_extend = -1
                        
                mc.setBlocks(
                    self.destination_point.x + x_to_extend,
                    self.destination_point.y,
                    self.origin_point.z,
                    self.destination_point.x - x_to_extend,
                    self.destination_point.y,
                    self.destination_point.z,
                    block.GLOWSTONE_BLOCK
                )
                mc.setBlocks(
                    self.destination_point.x + x_to_extend,
                    self.destination_point.y + 1,
                    self.origin_point.z,
                    self.destination_point.x - x_to_extend,
                    self.destination_point.y + 20,
                    self.destination_point.z,
                    0
                )

        elif slot == 'column':
            
            if abs(self.origin_point.z - self.destination_point.z) < abs(self.origin_point.y - self.destination_point.y):
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
                        # if self.origin_point.z < self.destination_point.z:
                        #     self.
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
                            self.origin_point.y + y_to_extend + 20,
                            self.origin_point.z + z_to_extend,
                            0
                        )
                        
                    
                        # if self.direction == "towards_next":
                        #     self.origin_point.x += 1
                        #     self.destination_point.x += 1
                        # else:
                        #     self.origin_point.x -= 1
                        #     self.destination_point.x -= 1
                
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
                            self.origin_point.y + y_to_extend + 20,
                            self.origin_point.z + z_to_extend,
                            0
                        )
                        
    
                        # if self.direction == "towards_next":
                        #     self.origin_point.x += 1
                        #     self.destination_point.x += 1
                        # else:
                        #     self.origin_point.x -= 1
                        #     self.destination_point.x -= 1
                    
                    
    
                # Straight line
                mc.setBlocks(
                    self.origin_point.x,
                    self.destination_point.y,
                    self.origin_point.z + z_to_extend,
                    x,
                    self.destination_point.y,
                    self.destination_point.z,
                    block.COBBLESTONE.id
                )
                mc.setBlocks(
                    self.origin_point.x,
                    self.destination_point.y + 1,
                    self.origin_point.z + z_to_extend,
                    x,
                    self.destination_point.y + 20,
                    self.destination_point.z,
                    0
                )
                
                # Center line
                
    
                if self.direction == "towards_next":
                    z_to_extend = 1  
                else:
                    z_to_extend = -1
                        

                mc.setBlocks(
                    x,
                    self.destination_point.y,
                    self.destination_point.z + z_to_extend,
                    self.destination_point.x,
                    self.destination_point.y,
                    self.destination_point.z - z_to_extend,
                    block.GLOWSTONE_BLOCK
                )

                
                mc.setBlocks(
                    x,
                    self.destination_point.y + 1,
                    self.destination_point.z + z_to_extend,
                    self.destination_point.x,
                    self.destination_point.y + 20,
                    self.destination_point.z - z_to_extend,
                    0
                )



                


        
        


if __name__ == '__main__':
    village = Village(mc, 150, 150)
    village.foundation_generator()
    village.road_generator('row')
    village.road_generator('column')