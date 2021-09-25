import mcpi.block as block 
from mcpi.vec3 import Vec3

class firelamp():
    def __init__(self, center_vector):
        self.layers = {
            '1st': [
                [Vec3(
                    center_vector.x,
                    center_vector.y + 1,
                    center_vector.z 
                ), (198, 0)]
            ],
            '2nd': [
                [Vec3(
                    center_vector.x,
                    center_vector.y + 2,
                    center_vector.z 
                ), (198, 0)]
            ],
            '3rd': [
                [Vec3(
                    center_vector.x,
                    center_vector.y + 3,
                    center_vector.z 
                ), (87, 0)]
            ],
            '4th': [
                # [Vec3(
                #     center_vector.x - 1,
                #     center_vector.y + 4,
                #     center_vector.z 
                # ), (95, 1)],
                # [Vec3(
                #     center_vector.x + 1,
                #     center_vector.y + 4,
                #     center_vector.z 
                # ), (95, 1)],                
                # [Vec3(
                #     center_vector.x,
                #     center_vector.y + 4,
                #     center_vector.z + 1 
                # ), (95, 1)],
                # [Vec3(
                #     center_vector.x,
                #     center_vector.y + 4,
                #     center_vector.z - 1 
                # ), (95, 1)],
                [Vec3(
                    center_vector.x,
                    center_vector.y + 4,
                    center_vector.z 
                ), (51, 0)]                
            ]
            # '5th': [
            #     [Vec3(
            #         center_vector.x,
            #         center_vector.y + 5,
            #         center_vector.z 
            #     ), (95, 1)]
            # ]
        }

    def build(self, mc):
        for layer in self.layers.values():
            for vector_info in layer:
                vector = vector_info[0]
                block = vector_info[1][0]
                block_tint = vector_info[1][1]
                mc.setBlock(vector, block, block_tint)


