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





# def set_vectors(self):
#         ''' Set vectors according to the player's rotation so that a village is generated right in front of him '''

#         vectors = {'northwest': None, 'northeast': None, 'southeast': None, 'southwest': None}
        
#         if 0 <= self.player_dir < 90:
#             vectors['northwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z - self.width_south_north)
#             vectors['northeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z - self.width_south_north)
#             vectors['southeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z)
#             vectors['southwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
#         elif 90 <= self.player_dir < 180:
#             vectors['northwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
#             vectors['northeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z)
#             vectors['southeast'] = Vec3(self.player_pos.x + self.width_east_west, 0, self.player_pos.z + self.width_south_north)
#             vectors['southwest'] = Vec3(self.player_pos.x, 0, self.player_pos.z + self.width_south_north)
#         elif 180 <= self.player_dir < 270:
#             vectors['northwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z)
#             vectors['northeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
#             vectors['southeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z + self.width_south_north)
#             vectors['southwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z + self.width_south_north)
#         else:
#             vectors['northwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z - self.width_south_north)
#             vectors['northeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z - self.width_south_north)
#             vectors['southeast'] = Vec3(self.player_pos.x, 0, self.player_pos.z)
#             vectors['southwest'] = Vec3(self.player_pos.x - self.width_east_west, 0, self.player_pos.z)

#         return vectors