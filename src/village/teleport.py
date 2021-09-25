from Village import Village

from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()

mc.player.setPos(pos.x + 500, 100, pos.z + 500)

if __name__ == '__main__':
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    mc.player.setPos(pos.x + 1000, 100, pos.z + 1000)
    user_input = input('Would you like to generate your vilalge here? [y/n]: ')
    while user_input != 'y':
        pos = mc.player.getTilePos()
        mc.player.setPos(pos.x + 1000, 100, pos.z + 1000)
        user_input = input('Would you like to generate your vilalge here? [y/n]: ')
    else:
        village = Village(mc)
        village.foundation_generator(mc)
        village.road_generator(mc, 'row')
        village.road_generator(mc, 'column')
        village.spawn_houses(mc)



