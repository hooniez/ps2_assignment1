from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()

mc.player.setPos(pos.x + 1000, 70, pos.z + 1000)