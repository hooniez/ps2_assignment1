# gamerule doDaylightCycle false
# time set 6000

# Uncomment 208 to 220 to generate foundations   only


from mcpi.minecraft import Minecraft
import random
import numpy as np
import mcpi.block as block # Find a proper way to stack this module as the same module is used in the main.py
from mcpi.vec3 import Vec3
from collections import Counter
import time

mc = Minecraft.create()

def clear_the_foundation(start_vector, end_vector):
        mc.setBlocks(start_vector.x, start_vector.y + 1, start_vector.z, end_vector.x, end_vector.y + 100 , end_vector.z, 0)

    # def get_most_common_block(start_vector, end_vector):
    #     # FIX ME when you need this method
    #     blocks = list(mc.getBlocks(start_vector, end_vector))
    #     blocks_counter = Counter(blocks)
    #     most_common_block = blocks_counter.most_common()[0][0]
    #     num_most_common_blocks = blocks_counter.most_common()[0][1]
        
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
    def __init__(self, width_south_north, width_east_west):
        ''' Cells generated from num_rows and num_columns make empty plots into which foundations can be generated one per each '''
        # self.adjacency_list = {}
        # self.road_distances = {}
        # From the perspective of a player's position (x, y, z), a village covers the square gap from (x + village_range_minus, z + village_range_minus) and (x + village_range_plus, z + village_range_plus)
        self.width_south_north = width_south_north
        self.width_east_west = width_east_west
        self.player_pos = mc.player.getTilePos()        
        self.player_dir = mc.player.getRotation()
        self.vectors = self.set_vectors()
        self.foundation_max_size = 21
        self.buffer_east_west_min = self.foundation_max_size // 5
        self.buffer_east_west_max = 3 * self.buffer_east_west_min
        self.buffer_south_north_min = 0
        self.buffer_south_north_max = self.foundation_max_size // 2 * 2
        self.foundation_wrappers = []
        self.foundation_width_spaces_between = []
        self.foundation_length_spaces_between = []
        self.foundation_longest_lengths = [0]

    def set_vectors(self):
        ''' Set vectors according to the player's rotation so that a village is generated right in front of him '''

        vectors = {'northwest': None, 'northeast': None, 'southeast': None, 'southwest': None}
        
        if 0 <= self.player_dir < 90:
            vectors['northwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z - self.width_south_north)
            vectors['northeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z - self.width_south_north)
            vectors['southeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z)
            vectors['southwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
        elif 90 <= self.player_dir < 180:
            vectors['northwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
            vectors['northeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z)
            vectors['southeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z + self.width_south_north)
            vectors['southwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z + self.width_south_north)
        elif 180 <= self.player_dir < 270:
            vectors['northwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z)
            vectors['northeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
            vectors['southeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z + self.width_south_north)
            vectors['southwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z + self.width_south_north)
        else:
            vectors['northwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z - self.width_south_north)
            vectors['northeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z - self.width_south_north)
            vectors['southeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
            vectors['southwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z)

        return vectors

    def random_grid_calculator(self):
        row = 0
        remaining_width = self.width_east_west 
        remaining_length = self.width_south_north
        foundation_wrapper_max_width = self.foundation_max_size + (2 * self.buffer_east_west_max)
        foundation_wrapper_max_length = self.foundation_max_size + self.buffer_south_north_max
        while remaining_length >= foundation_wrapper_max_length:
            longest_length = 0
            self.foundation_wrappers.append([])
            self.foundation_width_spaces_between.append([])
            remaining_width = self.width_east_west 
            while remaining_width >= foundation_wrapper_max_width:
                foundation_wrapper = Foundation_wrapper(self.buffer_east_west_min, self.buffer_east_west_max, self.buffer_south_north_min, self.buffer_south_north_max, self.foundation_max_size)
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

            



            



        
        
    # def add_house(self, new_house):
    #     self.adjacency_list[new_house] = []
        
    # def add_directed_road(self, from_house, to_house, road_distance):
    #     self.road_distances[(from_house, to_house)] = road_distance
    #     self.adjacency_list[from_house].append(to_house)
        
    # def add_undirected_road(self, house_a, house_b, road_distance):
    #     self.add_directed_road(house_a, house_b, road_distance)
    #     self.add_directed_road(house_b, house_a, road_distance)

#     def generate_x_y_and_z(self, player_range_minus, player_range_plus, foundation_width_S_N, foundation_width_E_W, boundary_coordinates=[]):
#         '''Generate random x and z coordinates'''
#         random_binary = random.randint(0, 1)
#         if random_binary == 0:
#             rand_x = random.randint(self.village_range_minus, player_range_minus)
#         else:
#             rand_x = random.randint(player_range_plus, self.village_range_plus)
#         random_binary = random.randint(0, 1)
#         if random_binary == 0:
#             rand_z = random.randint(self.village_range_minus, player_range_minus)
#         else:
#             rand_z = random.randint(player_range_plus, self.village_range_plus)
#         ground_height = get_height_actual_block(self.player_pos_x + rand_x, self.player_pos_z + rand_z)
    
#         # Make sure the next rand_x and rand_z don't fall near the previous. 
#         # The same amount of space taken up by a house  will be padded all around the house, forming a square boundary.
#         for i in range(len(boundary_coordinates)):
#             if (boundary_coordinates[i][0][0]<= rand_x <= boundary_coordinates[i][1][0] and boundary_coordinates[i][0][1] <= rand_z <= boundary_coordinates[i][1][1]) or (boundary_coordinates[i][0][0]<= rand_x + foundation_width_E_W <= boundary_coordinates[i][1][0] and boundary_coordinates[i][0][1] <= rand_z + foundation_width_S_N <= boundary_coordinates[i][1][1]):
#                 rand_x, ground_height, rand_z = self.generate_x_y_and_z(player_range_minus, player_range_plus, foundation_width_S_N, foundation_width_E_W)
    
#         boundary_coordinates.append(( (rand_x - foundation_width_E_W, rand_z - foundation_width_S_N), (rand_x + (2 * foundation_width_E_W), rand_z + (2 * foundation_width_S_N)) ))

#         print("randomly generated x, y, and z are: {}, {}, {}".format(rand_x, ground_height, rand_z))        
    
#         return rand_x, ground_height, rand_z
    
    def foundation_generator(self):
        ''' Inside a square excluding 3 x 3 square near the player, plant a foundation. Exclude the area taken up by the first foundation from the initial square and plant another; In the same way, plant many more. '''

        self.random_grid_calculator()
        
        current_z = self.player_pos.z + 1
        for idx_r, row in enumerate(self.foundation_wrappers):
            current_x = self.player_pos.x + 1
            current_z += self.foundation_longest_lengths[idx_r] + 1
            for idx_f, foundation_wrapper in enumerate(row):
                # You need to add even values here since foundation has its starting block to which these numbers will be added
                x = current_x + foundation_wrapper.buffer_right_width + 1
                z = current_z + foundation_wrapper.buffer_bottom_length + 1
                y = get_height_actual_block(x,z)
                foundation = Foundation(x, y, z)
                foundation_wrapper.foundation = foundation
                
                # # foundation_conatiner
                # lay_foundation(Vec3(current_x + foundation_wrapper.buffer_right_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.BRICK_BLOCK.id)
                # # buffer_right
                # lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), 
                # Vec3(current_x + foundation_wrapper.buffer_right_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.WOOL.id)
                # # buffer_left
                # lay_foundation(Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length),
                #  Vec3(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, get_height_actual_block(current_x + foundation_wrapper.buffer_right_width + foundation_wrapper.foundation_container_width + foundation_wrapper.buffer_left_width, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), block.WOOL.id)
                # #buffer_bootm                
                # lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z), current_z), Vec3(current_x + foundation_wrapper.buffer_bottom_width, get_height_actual_block(current_x + foundation_wrapper.buffer_bottom_width, current_z + foundation_wrapper.buffer_bottom_length), current_z + foundation_wrapper.buffer_bottom_length), block.DIAMOND_BLOCK)
                # #buffer_top
                # lay_foundation(Vec3(current_x, get_height_actual_block(current_x, current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length), current_z + foundation_wrapper.buffer_bottom_length + foundation_wrapper.foundation_container_length),
                #  Vec3(current_x + foundation_wrapper.width, get_height_actual_block(current_x + foundation_wrapper.width, current_z + foundation_wrapper.length), current_z + foundation_wrapper.length), block.LAPIS_LAZULI_BLOCK)
                
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
                            previous_foundation_wrapper = column[idx - 1]
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

                            
        
                            
                            
                            
                            
                            
            
                            
    
                            
                            
    
            
        
                            
                            
                            
    

    


            

                

                
                    
                     

            


                
                     




class Foundation_wrapper():
    def __init__(self, buffer_east_west_min, buffer_east_west_max, buffer_south_north_min, buffer_south_north_max, foundation_max_size):
        self.buffer_left_width = random.randint(buffer_east_west_min, buffer_east_west_max)
        self.buffer_left_length = foundation_max_size
        self.buffer_right_width = random.randint(buffer_east_west_min, buffer_east_west_max)
        self.buffer_right_length = foundation_max_size
        self.buffer_bottom_width = foundation_max_size + self.buffer_left_width + self.buffer_right_width
        self.buffer_bottom_length = random.randint(buffer_south_north_min, buffer_south_north_max)
        self.buffer_top_width = foundation_max_size + self.buffer_left_width + self.buffer_right_width
        self.buffer_top_length = random.randint(buffer_south_north_min, buffer_south_north_max - self.buffer_bottom_length)
        self.foundation_container_width = foundation_max_size
        self.foundation_container_length = foundation_max_size
        self.width = self.buffer_bottom_width
        self.length = self.buffer_top_length + self.buffer_left_length + self.buffer_bottom_length
        self.foundation = None
        # self.foundation = Foundation()




class Foundation():
    # half the blocks > AIR = Stop layering
    def __init__(self, x, y, z):
        self.width_east_west = random.randrange(12, 20, 2) 
        self.width_south_north = random.randrange(12, 20, 2) 
        # vectors stores random vector and west, northwest, north relative to the random vector
        self.vectors = {'southeast': Vec3(x, get_height_actual_block(x,z), z), 'southwest': Vec3(x + self.width_east_west, get_height_actual_block(x + self.width_east_west ,z), z), 'northwest': Vec3(x + self.width_east_west, get_height_actual_block(x + self.width_east_west, z + self.width_south_north), z + self.width_south_north), 'northeast': Vec3(x, get_height_actual_block(x, z + self.width_south_north), z + self.width_south_north)}
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

    # def get_most_common_block(start_vector, end_vector):
    #     # FIX ME when you need this method
    #     blocks = list(mc.getBlocks(start_vector, end_vector))
    #     blocks_counter = Counter(blocks)
    #     most_common_block = blocks_counter.most_common()[0][0]
    #     num_most_common_blocks = blocks_counter.most_common()[0][1]
        
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
                        
    
                        # Descend
                        # if self.origin_point.z < self.destination_point.z:
                        #     self.
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
                        
                    
                        # if self.direction == "towards_next":
                        #     self.origin_point.x += 1
                        #     self.destination_point.x += 1
                        # else:
                        #     self.origin_point.x -= 1
                        #     self.destination_point.x -= 1
                
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
                        
    
                        # if self.direction == "towards_next":
                        #     self.origin_point.x += 1
                        #     self.destination_point.x += 1
                        # else:
                        #     self.origin_point.x -= 1
                        #     self.destination_point.x -= 1
                    
                    
    
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
    village = Village(150, 150)
    village.foundation_generator()
    village.road_generator('row')
    village.road_generator('column')