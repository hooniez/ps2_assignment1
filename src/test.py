from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block
from direction import Direction
from path import Path as path

mc = Minecraft.create()
player = mc.player.getDirection()
print(player)
print(Direction.getCardinalDirection(player))
print(Direction.getDirection(player))

tile = mc.player.getTilePos()
print(f"player pos: {tile}")
print(f"start: {Vec3(tile.x, tile.y, tile.z - 1)}")
print(f"end: {Vec3(tile.x, tile.y + 10, tile.z - 11)}")

path._layStairCase(Vec3(tile.x, tile.y, tile.z - 1), Vec3(tile.x, tile.y + 10, tile.z - 11), block.COBBLESTONE, mc) #go north
path._layStairCase(Vec3(tile.x + 1, tile.y, tile.z), Vec3(tile.x + 11, tile.y + 10, tile.z), block.COBBLESTONE, mc) #go east
path._layStairCase(Vec3(tile.x, tile.y, tile.z + 1), Vec3(tile.x, tile.y + 10, tile.z + 11), block.COBBLESTONE, mc) #go south
path._layStairCase(Vec3(tile.x - 1, tile.y, tile.z), Vec3(tile.x - 11, tile.y + 10, tile.z), block.COBBLESTONE, mc) #go west
