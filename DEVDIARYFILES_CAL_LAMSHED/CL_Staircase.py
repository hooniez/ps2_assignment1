# Server commands to suspend time:
# gamerule doDaylightCycle false
# time set day

from mcpi.minecraft import Minecraft

# So that we can refer to block types by name, rather than ID:
from mcpi import block

mc = Minecraft.create()

# Get player's exact coordinates
#p_x, p_y, p_z = mc.player.getPos()

# Get player tile pos (i.e., values rounded to nearest integer)
playerTilePos = mc.player.getTilePos()

# Place a brick, offset 5 units in the x-direction from the player
xsize = 20
zsize = 4
# mc.setBlock(playerTilePos.x,playerTilePos.y,playerTilePos.z,block.BRICK_BLOCK)
for i in range(xsize,-1,-1):
    print(i)
    mc.setBlocks(playerTilePos.x + 5, \
                    playerTilePos.y + xsize-i, \
                        playerTilePos.z, \
                            playerTilePos.x + 5 + i, \
                                playerTilePos.y + xsize-i, \
                                    playerTilePos.z+zsize, \
                                        block.BRICK_BLOCK)

