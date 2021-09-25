import random
from mcpi.vec3 import Vec3
import mcpi.block as block 

class Foundation():
    # half the blocks > AIR = Stop layering
    def __init__(self,mc, width_x, width_z, x, y, z):
        self.width_x = width_x
        self.width_z = width_z
        # vectors stores random vector and west, northwest, north relative to the random vector
        self.vectors = {
            'southeast': Vec3(x, mc.getHeight(x,z), z),
            'southwest': Vec3(x + self.width_x, mc.getHeight(x + self.width_x ,z), z),
            'northwest': Vec3(x + self.width_x, mc.getHeight(x + self.width_x, z + self.width_z), z + self.width_z),
            'northeast': Vec3(x, mc.getHeight(x, z + self.width_z), z + self.width_z)
        }
        self.start_vector = None
        self.end_vector = None
        self.center_vector = None
        self.highest_vector = None
        self.building_block = block.GRASS.id
        self.house = None
    
    def toString(self):
        return f"vectors = {self.vectors}"

            
    def position_vectors(self):
        # Find the vector with the highest y-axis and set every vector's height to it 
        # Assign start_vector, end_vector, and center_vector with values.

    
        highest_vector_val = self.vectors['southeast'].y    
        for key, vec in self.vectors.items():
            vector_val = vec.y
            if  vector_val > highest_vector_val:
                highest_vector_val = vector_val

        # Set each height to the highest height
        for vector in self.vectors.values():
            vector.y = highest_vector_val

        self.start_vector = self.vectors['southeast']
        self.end_vector = self.vectors['northwest']
        self.center_vector = Vec3((self.start_vector.x + self.end_vector.x) / 2, self.start_vector.y, (self.start_vector.z + self.end_vector.z) / 2)


    def clear_the_foundation(self, mc):
        mc.setBlocks(self.start_vector.x, self.start_vector.y + 1, self.start_vector.z, self.end_vector.x, self.end_vector.y + 100 , self.end_vector.z, 0)
        
    def lay_foundation(self, mc):
        self.position_vectors()
        mc.setBlocks(self.start_vector, self.end_vector, self.building_block)
        
        for vec in self.vectors.values():
            mc.setBlocks(vec.x, vec.y - 1, vec.z, vec.x, vec.y - 150, vec.z, self.building_block)

        self.clear_the_foundation(mc)
        self.mark_start_end_vectors(mc)
    
    # for  testing only
    # def mark_start_end_vectors(self, mc):
    #     mc.setBlock(self.start_vector.x, self.start_vector.y + 5, self.start_vector.z, block.SANDSTONE)
    #     mc.setBlock(self.end_vector.x, self.end_vector.y + 5, self.end_vector.z, block.END_STONE)
