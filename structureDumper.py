
import nbt
import sys

if __name__ == '__main__' :

	with open(sys.argv[1], 'rb') as fd :
		tree = nbt.NBTFile(buffer=fd)
		print(tree.pretty_tree())

