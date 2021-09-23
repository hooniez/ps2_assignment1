import csv
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

mc = Minecraft.create()

pos = mc.player.getTilePos()
pos = Vec3(pos.x + 1, pos.y, pos.z + 1)



# contents = [name, z_width, x_width, y_height, size, blocks]

with open('save_blocks.csv', 'r') as f:
    rows = csv.reader(f)
    for row in rows:
        print(row)
        name, z_width, x_width, y_height, size, blocks = row
        z_width = int(z_width)
        x_width = int(x_width)
        y_height = int(y_height)
        size = int(size)
        blocks = list(map(int, blocks.split()))



i = 0    
for y in range(y_height + 1):
    for x in range(x_width):      
        for z in range(z_width):
            mc.setBlock(
                pos.x + x,
                pos.y + y,
                pos.z + z,
                blocks[i], blocks[i + 1]
            )
            i += 2
