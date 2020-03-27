
import nbt
import sys

if __name__ == '__main__' :

	with open(sys.argv[1], 'rb') as fd :
		tree = nbt.NBTFile(buffer=fd)
		print(tree.pretty_tree())
		x, y , z  = tree['size']
		blocks, logged = tree['structure']['block_indices']
		
		i = 0
		blockPalette = tree['structure']['palette']['default']['block_palette']
		for xx in range(int(x)):
			for yy in range(int(y)):
				for zz in range(int(z)):
					print("x : %d, y:%s, z:%s -> %s"%(xx,yy,zz, blockPalette[int(blocks[i])]))
					i+=1


