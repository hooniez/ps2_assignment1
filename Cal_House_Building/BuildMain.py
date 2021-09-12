import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import buildHouse

mc = minecraft.Minecraft.create()
p = mc.player.getTilePos()

houseLocation = p

houseWidth = 10
houseHeight = 5
houseLength = 10
gap = 3
# mc.setBlocks(p.x+1,p.y,p.z+1,p.x+10,p.y+5,p.z+10,block.ICE)
# prop = buildHouse.house_property(p,12,12)
# prop.drawProperty(mc)
# myHouse = buildHouse.house(prop,5)
# myHouse.createRoomSimple()
# for room in myHouse.rooms:
#     room.drawRoom(mc)
prop = buildHouse.house_property(p,30,30)
prop.drawProperty(mc)
roomsize = 8
roomheight = 2
myHouse = buildHouse.house2(prop)
myHouse.createEmptyHouse(roomheight,roomsize) # specify the room size, currently only squares
myHouse.addRoom(mc)
myHouse.addRoom(mc)
myHouse.addRoom(mc)
myHouse.addRoom(mc)
myHouse.addRoom(mc)