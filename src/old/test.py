from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block
from direction import Direction
from path import Path as path
import math
from numpy import linspace
from pathlib import Path
import csv
import itertools
import datetime


def getTopBlock(lower, upper):
    myBlocks = mc.getBlocks(
        lower.x,
        lower.y,
        lower.z,
        upper.x,
        upper.y,
        upper.z,
    )

    area = [b for b in myBlocks]
    
    cols = []
    cols.append(area[::5])
    cols.append(area[1::5])
    cols.append(area[2::5])
    cols.append(area[3::5])
    cols.append(area[4::5])

    writer = csv.writer(open(Path('test.csv'), 'w', newline=""), delimiter=',')
    print(cols)
    writer.writerows(cols)

    # myBlocksList = list(reversed())
    # blockPlace = None

    # for index, b in enumerate(myBlocksList):
    #     if b not in [block.AIR.id, block.WOOD.id, block.LEAVES.id, block.LEAVES2.id, 31, 32, 37, 38, 39, 40, 51, 59, 83, 86, 103, 106, 161, 162, 175, 176]:
    #         blockPlace = Vec3(
    #             end.x,
    #             end.y - index,
    #             end.z
    #         )
    #         break

    # print(blockPlace)

    # return blockPlace


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    mc = Minecraft.create()
    player = mc.player.getDirection()
    direction = Direction.getCardinalDirection(player)


    tile = mc.player.getTilePos()
    print(tile)

    

    if direction == Direction.SOUTH:
        for i in range(50):
            start = Vec3(tile.x - 2, -60, (tile.z + 1) + i)
            end = Vec3(tile.x + 3, 60, (tile.z + 1) + i)

            blockPlace = getTopBlock(start, end)
            # mc.setBlock(blockPlace.x, blockPlace.y, blockPlace.z, block.BRICK_BLOCK.id)

    elif direction == Direction.EAST:
        for j in range(5):
            for i in range(50):
                start = Vec3((tile.x + 1) + i, -60, tile.z + j)
                end = Vec3((tile.x + 1) + i, 60, tile.z + j)

                blockPlace = getTopBlock(start, end)
                # mc.setBlock(blockPlace.x, blockPlace.y, blockPlace.z, block.BRICK_BLOCK.id)

    elif direction == Direction.WEST:
        for j in range(5):
            for i in range(50):
                start = Vec3((tile.x - 1) - i, -60, tile.z - j)
                end = Vec3((tile.x - 1) - i, 60, tile.z - j)

                blockPlace = getTopBlock(start, end)
                # mc.setBlock(blockPlace.x, blockPlace.y, blockPlace.z, block.BRICK_BLOCK.id)

    elif direction == Direction.NORTH:
        for j in range(5):
            for i in range(50):
                start = Vec3(tile.x - j, -60, (tile.z - 1) - i)
                end = Vec3(tile.x - j, 60, (tile.z - 1) - i)

                blockPlace = getTopBlock(start, end)
                # mc.setBlock(blockPlace.x, blockPlace.y, blockPlace.z, block.BRICK_BLOCK.id)

    endTime = datetime.datetime.now()

    time_diff = (endTime - startTime)
    execution_time = time_diff.total_seconds()
    print(f"runtime: {execution_time}")
