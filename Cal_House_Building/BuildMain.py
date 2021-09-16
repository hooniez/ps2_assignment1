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
roomSize = 8
floorHeight = 4
myHouse = buildHouse.house(prop,floorHeight,roomSize)
myHouse.createFloor() # specify the room size, currently only squares
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc)
myHouse.floors[0].addRoom(mc,'pool')
myHouse.floors[0].addDoors(mc)
myHouse.floors[0].addFrontDoor(mc)
# Building a new level