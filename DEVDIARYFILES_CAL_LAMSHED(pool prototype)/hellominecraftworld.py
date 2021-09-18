import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()
mc.postToChat("hello world")
mc.player.setPos(0, 100, 0)