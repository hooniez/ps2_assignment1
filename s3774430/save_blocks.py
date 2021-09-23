import csv
from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()
pos = Vec3(pos.x + 1, pos.y, pos.z + 1)

name = input('What furniture is this? ')
z_width = int(input('type in z width: '))
x_width = int(input('type in x width: '))
y_height = int(input('type in y height: '))

size = x_width * z_width * y_height

blocks = []




for y in range(y_height + 1):
    for x in range(x_width):      
        for z in range(z_width):
            block = mc.getBlockWithData(
                pos.x + x,
                pos.y + y,
                pos.z + z
            )
            block_with_data = list(block)
            blocks.append(block_with_data[0])
            blocks.append(block_with_data[1])

blocks = list(map(str, blocks))

blocks = ' '.join(blocks)

contents = [name, z_width, x_width, y_height, size, blocks]

with open('save_blocks.csv', 'a') as f:
    file_writer = csv.writer(f)
    file_writer.writerow(contents)