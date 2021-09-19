from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()

block = mc.getBlock(
    pos.x,
    pos.y - 1,
    pos.z 
)

print(block)

mc.setBlock(
    pos.x,
    pos.y + 3,
    pos.z,
    block
)
