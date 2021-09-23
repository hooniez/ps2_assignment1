from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()

mc.setBlocks(
    pos.x,
    pos.y + 50,
    pos.z,
    pos.x + 50,
    pos.y + 50,
    pos.z + 50,
    42
)

mc.player.setPos(
    pos.x + 1,
    pos.y + 50,
    pos.z + 1
)

mc.setBlock(
    pos.x + 3,
    pos.y + 50,
    pos.z,
    138
)

mc.setBlock(
    pos.x,
    pos.y + 50,
    pos.z + 3,
    155
)