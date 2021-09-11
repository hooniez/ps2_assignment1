# Server commands to suspend time:
# gamerule doDaylightCycle false
# time set day

from mcpi.minecraft import Minecraft
import mcpi.block as block
import time

mc = Minecraft.create()

# Get player's exact coordinates
pos = mc.player.getTilePos()

teleport_val = 40000

# Move him away from where he spawns
mc.player.setPos(pos.x + teleport_val , mc.getHeight(pos.x + teleport_val, pos.z + teleport_val), pos.z + teleport_val)
pos = mc.player.getTilePos()

time.sleep(3)

falls_to_the_hell = 60
steps_to_the_sky = falls_to_the_hell * 2

# Bring the player down to the far void
mc.player.setPos(pos.x, -falls_to_the_hell, pos.z)
pos = mc.player.getTilePos()


time.sleep(3)

# Create an exit
for i in range(steps_to_the_sky):

    mc.setBlocks(
        pos.x + i, 
        pos.y - 1 + i, 
        pos.z, 
        pos.x + i, 
        pos.y + steps_to_the_sky, 
        pos.z + 1, 
        block.AIR
    )
    
    mc.setBlocks(
        pos.x + i, 
        pos.y - 1 + i, 
        pos.z, 
        pos.x + i, 
        pos.y - 1 + i, 
        pos.z + 1, 
        block.STAIRS_COBBLESTONE
    )







