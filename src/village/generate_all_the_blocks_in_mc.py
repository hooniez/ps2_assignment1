from mcpi.minecraft import Minecraft
import mcpi.block as block 

mc = Minecraft.create()

pos = mc.player.getTilePos()

x = pos.x
y = pos.y
z = pos.z

x_to_extend = 16
x_to_contract = -1
z_to_extend = 17
z_to_contract = -1

mc.setBlocks(
    x + x_to_contract,
    y - 1,
    z + z_to_contract,
    x + x_to_extend,
    y - 1,
    z + z_to_extend,
    block.GLASS.id
)

mc.setBlocks(
    x + x_to_contract,
    y,
    z + z_to_contract,
    x + x_to_extend,
    y,
    z + z_to_contract,
    block.GLASS.id
)

mc.setBlocks(
    x + x_to_contract,
    y,
    z + z_to_contract,
    x + x_to_contract,
    y,
    z + z_to_extend,
    block.GLASS.id

)

mc.setBlocks(
    x + x_to_extend,
    y,
    z + z_to_contract,
    x + x_to_extend,
    y,
    z + z_to_extend,
    block.GLASS.id

)

mc.setBlocks(
    x + x_to_contract,
    y,
    z + z_to_extend,
    x + x_to_extend,
    y,
    z + z_to_extend,
    block.GLASS.id

)


original_x = x
original_y = y
original_z = z
for i in range(300):
    mc.setBlock(x, y, z, i)
    x += 1
    if (i != 0) & (i % 15 == 0):
        x = original_x
        z += 1