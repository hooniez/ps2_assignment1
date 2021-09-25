from mcpi.minecraft import Minecraft
mc = Minecraft.create()
from mcpi import block

p_x, p_y, p_z = mc.player.getPos()

p = mc.player.getTilePos()

for i in range(0,25):
    mc.setBlocks(p.x + 5, p.y, p.z+5,p.x,p.y,p.z, block.BRICK_BLOCK)
    p.x=p.x+1
    p.y=p.y+1

