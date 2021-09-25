from mcpi.minecraft import Minecraft
import mcpi.block as block 

# The first row's first block's id is 1
# The first row's last block's id is 10
    
def main(mc):
    pos = mc.player.getTilePos()
    
    x = pos.x
    y = pos.y
    z = pos.z
    
    x_to_extend = 10
    x_to_contract = -1
    z_to_extend = 26
    z_to_contract = -1
    
    # Floor
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
    for i in range(1, 300):
        mc.setBlock(x, y, z, i)
        x += 1
        if i % 10 == 0:
            x = original_x
            z += 1
    
if __name__ == '__main__':
    mc = Minecraft.create()
    main(mc)