
# Building a new level


def HouseScript():
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    import random
    import buildHouse
    mc = minecraft.Minecraft.create()
    p = mc.player.getTilePos()

    houseLocation = p
    prop = buildHouse.house_property(p,30,30)
    prop.drawProperty(mc)
    roomSize = 8
    floorHeight = 5

    myHouse = buildHouse.house(prop,floorHeight,roomSize)

    myHouse.createFloor() # specify the room size, currently only squares
    FirstFloorRoomNumber = 6

    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc)
    myHouse.floors[0].addRoom(mc,'pool')
    myHouse.floors[0].addDoors(mc)
    myHouse.floors[0].addFrontDoor(mc)
    print('---------')


    myHouse.createFloor()


    myHouse.floors[1].addRoom(mc)
    myHouse.floors[1].addRoom(mc,'pool')
    myHouse.floors[1].addRoom(mc)
    myHouse.floors[1].addDoors(mc)

    myHouse.createFloor()
    myHouse.floors[2].addRoom(mc)
    myHouse.floors[2].addRoom(mc)
    myHouse.floors[2].addDoors(mc)

    myHouse.addAllStairs(mc)

if __name__ == '__main__':
    HouseScript()
else:
    print('Imported as Module')