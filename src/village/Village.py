from mcpi.minecraft import Minecraft
import random
import numpy as np
import mcpi.block as block 
from mcpi.vec3 import Vec3
from Foundation_wrapper import Foundation_wrapper
from Foundation import Foundation
from Road import Road
from house import House
from land import Property

''' 
    Let's get some terminology out of the way. 
    Width refers to the number of blocks in x-axis
    Length refers to the number of blocks in z-axis
    When width is used instead of length for z value, it will be suffixed with z. (e.g. width_z)
'''

class Village():
    def __init__(self, mc):
        ''' Cells generated from num_rows and num_columns make empty plots into which foundations can be generated one per each '''
        self.foundation_size_min = 20
        self.foundation_size_max = 40
        
        # Village size
        self.width_z = self.foundation_size_max * 10
        self.width_x = self.foundation_size_max * 10

        self.buffer_x_min = self.foundation_size_min // 5
        self.buffer_x_max = self.buffer_x_min * 2
        self.buffer_z_min = 0
        self.buffer_z_max = self.foundation_size_max

        self.foundation_wrappers = [] 
        self.foundation_width_spaces_between = []
        self.foundation_length_spaces_between = []
        self.foundation_longest_lengths = [0]

        self.player_pos = mc.player.getTilePos()

        self.road_width = 3
        

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
        self.lay_blocks_and_clear_the_surface(
            Vec3(
                current_x + foundation_wrapper.buffer_right_width, 
                mc.getHeight(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length),
                current_z + foundation_wrapper.buffer_bottom_length
            ),
            Vec3(
                current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width,
                mc.getHeight(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
                current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length
            ),
            block.BRICK_BLOCK.id
        )

        # buffer_right
        self.lay_blocks_and_clear_the_surface(
            Vec3(
                current_x, 
                mc.getHeight(current_x, current_z + foundation_wrapper.buffer_bottom_length),
                current_z + foundation_wrapper.buffer_bottom_length
            ), 
            Vec3(
                current_x + foundation_wrapper.buffer_right_width,
                mc.getHeight(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
                current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
                block.WOOL.id
            )

        # buffer_left
        self.lay_blocks_and_clear_the_surface(
            Vec3(
                current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width,
                mc.getHeight(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length),
                current_z + foundation_wrapper.buffer_bottom_length
            ),
         Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, mc.getHeight(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.WOOL.id)
        #buffer_bootm                
        self.lay_blocks_and_clear_the_surface(Vec3(current_x, mc.getHeight(current_x, current_z), current_z), Vec3(current_x + foundation_wrapper.buffer_bottom_width, mc.getHeight(current_x + foundation_wrapper.buffer_bottom_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), block.DIAMOND_BLOCK)
        #buffer_top
        self.lay_blocks_and_clear_the_surface(Vec3(current_x, mc.getHeight(current_x, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
         Vec3(current_x + foundation_wrapper.width, mc.getHeight(current_x + foundation_wrapper.width, current_z + foundation_wrapper.length), current_z + foundation_wrapper.length), block.LAPIS_LAZULI_BLOCK)


    def foundation_generator(self, mc):
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

                width_x = random.randrange(self.foundation_size_min, self.foundation_size_max, 2)
                width_z = random.randrange(self.foundation_size_min, self.foundation_size_max, 2)

                foundation = Foundation(mc, width_x, width_z, x, y, z)
                foundation_wrapper.foundation = foundation

                

                # self.visualise_grid(current_x, current_z, foundation_wrapper)

                foundation.lay_foundation(mc)
                
                if idx_f != len(row) - 1:
                    current_x += (foundation_wrapper.width + self.foundation_width_spaces_between[idx_r][idx_f] + 1)


    def road_generator(self, mc, section):
        if section == "row":
            pass
        elif section == 'column':
            # Make sure all rows have the same number of foundations
            max_foundations = len(self.foundation_wrappers[0])
            for row in self.foundation_wrappers:
                if max_foundations < len(row):
                    max_foundations = len(row)
            for row in self.foundation_wrappers:
                while len(row) < max_foundations:
                    row.append(None)

            np_foundation_wrappers = np.array(self.foundation_wrappers, dtype='object')
            self.foundation_wrappers = np_foundation_wrappers.T.tolist()

        for foundation_wrapper in self.foundation_wrappers:
            for idx, current_foundation_wrapper in enumerate(foundation_wrapper):
                current_foundation = current_foundation_wrapper.foundation


                if idx != len(foundation_wrapper) - 1:
                    next_foundation_wrapper = foundation_wrapper[idx+ 1]
                    next_foundation = next_foundation_wrapper.foundation
                    road_mid_point_between_current_and_next = Vec3(
                        (current_foundation.end_vector.x + next_foundation.start_vector.x) // 2,
                        (current_foundation.end_vector.y + next_foundation.start_vector.y) // 2,
                        (current_foundation.end_vector.z + next_foundation.start_vector.z) // 2
                    )

                    origin_vector = current_foundation.end_vector
                    destination_vector = road_mid_point_between_current_and_next
                    direction = "towards_next"
                    
                    road = Road(mc, origin_vector, destination_vector, direction, self.road_width)
                    road.lay_road(mc, section)


                if idx != 0:
                    previous_foundation_wrapper = foundation_wrapper[idx - 1]
                    previous_foundation = previous_foundation_wrapper.foundation 
                    
                    road_mid_point_between_current_and_previous = Vec3(
                        (current_foundation.start_vector.x + previous_foundation.end_vector.x) // 2,
                        (current_foundation.start_vector.y + previous_foundation.end_vector.y) // 2,
                        (current_foundation.start_vector.z + previous_foundation.end_vector.z) // 2
                    )   

                    origin_vector = current_foundation.start_vector
                    destination_vector = road_mid_point_between_current_and_previous
                    direction = "towards_previous"

                    road = Road(mc, origin_vector, destination_vector, direction, self.road_width)
                    road.lay_road(mc, section)


                


    def lay_blocks_and_clear_the_surface(self, start_vector, end_vector, building_block):
        mc.setBlocks(start_vector, end_vector, building_block)
        mc.setBlocks(start_vector.x, start_vector.y + 1, start_vector.z, end_vector.x, end_vector.y + 100 , end_vector.z, 0)


    def spawn_houses(self, mc):
        for wrapperList in self.foundation_wrappers:
            for wrapper in wrapperList:
                print(wrapper.foundation)
                if wrapper is not None:
                    wrapper.foundation.house = House(Property(wrapper.foundation))
                    wrapper.foundation.house.generateHouse(mc)


if __name__ == '__main__':
    mc = Minecraft.create()
    village = Village(mc)
    village.foundation_generator(mc)
    village.road_generator(mc,'row')
    village.road_generator(mc,'column')
    village.spawn_houses(mc)