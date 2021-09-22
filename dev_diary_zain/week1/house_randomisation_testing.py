
from mcpi import minecraft
from time import sleep
from mcpi import block
import random

mc = minecraft.Minecraft.create()

randmain = random.randint(1,2)
randside = random.randint(0,2)


def main_room1(x,y,z):
    x,y,z = x-3, y, z-5
    y = mc.getHeight(x,z)
    y = y+1
    global mcentre1
    mcentre1 = x,y,z
    mc.setBlocks(x-5,y-1,z+4,x+5,y+4,z-4,45)
    mc.setBlocks(x-4,y,z+3,x+4,y+3,z-3,0)
    mc.setBlocks(x+3,y,z+4,x+2,y+1,z+4,0)
    mc.setBlocks(x,y+1,z+4,x-4,y+2,z+4,20)

def main_room2(x,y,z):
    x,y,z = x,y,z-6
    y = mc.getHeight(x,z)
    y = y+1
    global mcentre2
    mcentre2 = x,y,z
    mc.setBlocks(x+4,y-1,z+5,x-4,y+5,z-5,155)
    mc.setBlocks(x+3,y,z+4,x-3,y+4,z-4,0)
    mc.setBlocks(x-1,y,z+5,x+1,y+2,z+5,0)

def side_room1(x,y,z):
    if randmain == 1:
        x,y,z = mcentre1
    elif randmain == 2:
        x,y,z = mcentre2

    while mc.getBlock(x,y,z) == 0:
        x = x-1
    mc.setBlocks(x,y,z,x,y+1,z,0)
    x,y,z = x-1,y,z
    mc.setBlocks(x,y-1,z-6,x-7,y+2,z+2,block.SANDSTONE,[2])
    mc.setBlocks(x,y,z-5,x-6,y+1,z+1,0)
    mc.setBlocks(x-1,y,z+2,x-2,y+1,z+2,0)
    mc.setBlocks(x-5,y,z+2,x-6,y+1,z+2,0)

def side_room2(x,y,z):
    if randmain == 1:
        x,y,z = mcentre1
    elif randmain == 2:
        x,y,z = mcentre2

    while mc.getBlock(x,y,z) == 0:
        x = x+1
    mc.setBlocks(x,y,z-1,x,y+1,z-1,0)
    #pool assignment
    x,y,z = x+4,y,z

    #fencing
    mc.setBlocks(x-3,y,z-5,x+5,y,z+5,139)
    mc.setBlocks(x-3,y,z-4,x+4,y,z+4,0)
    mc.setBlocks(x-3,y,z+5,x-1,y,z+4,0)

    #pool
    #stone
    mc.setBlocks(x+5,y-1,z+5,x-1,y-6,z-5,1)
    mc.setBlocks(x-3,y-1,z-5,x-1,y-6,z+5,1)
    #water
    mc.setBlocks(x+4,y-1,z+4,x,y-5,z-4,9)

def stair(x,y,z):

        if randmain == 1:
            x,y,z = mcentre1
        elif randmain == 2:
            x,y,z = mcentre2

        #finding top corner
        while mc.getBlock(x,y,z) == 0:
            y = y+1
        while mc.getBlock(x,y,z) != 0:
            z = z-1
        z = z+1
        while mc.getBlock(x,y,z) != 0:
            x = x+1
        x = x-1
        #abc == top corner
        a,b,c = x,y,z
        #making top corner hole
        z = z+2
        x = x-2
        mc.setBlocks(x,y,z-1,x+1,y,z+2,block.AIR)

        #stairs
        x = a-1
        z = c+1

        while mc.getBlock(x,y,z) == 0:
            mc.setBlocks(x,y,z,x-1,y,z,block.NETHER_BRICK)
            z= z+1
            y = y-1


a,b,c = mc.player.getPos()

if randmain == 1:
    main_room1(a,b,c)
elif randmain == 2:
    main_room2(a,b,c)


if randside == 1:
    side_room1(a,b,c)
elif randside == 2:
    side_room2(a,b,c)
elif randside == 0:
    stair(a,b,c)




