

import os
import leveldb
import argparse
from hsa import HSA, HSAType, Position, Dimension, Rectangle
from leveldb import Row, setLdb, Key

CHUNKSIZE=16
HSATAG=57

def getArgParser():
	parser = argparse.ArgumentParser(description="Minecraft Bedrock admin toolkit")
	parser.add_argument("--lib"			, type=str, help="Path to leveldb MCPE lib (dll or so file) (from https://github.com/Mojang/leveldb-mcpe)")
	parser.add_argument("--type", "-t"	 , type=str, required=True, help="Structure type (hut, fortress, monument, outpost)")
	parser.add_argument("--dimension", "-d", type=str, required=True, help="Dimension of the structure (overworld, nether, end)")
	parser.add_argument("--startX", "-x"   , type=int, required=True, help="Starting x of the structure")
	parser.add_argument("--startY", "-y"   , type=int, required=True, help="Starting y of the structure")
	parser.add_argument("--startZ", "-z"   , type=int, required=True, help="Starting z of the structure")
	parser.add_argument("--endX"		   , type=int, required=True, help="Ending x of the structure")
	parser.add_argument("--endY"		   , type=int, required=True, help="Ending y of the structure")
	parser.add_argument("--endZ"		   , type=int, required=True, help="Ending z of the structure")
	parser.add_argument("world"			, type=str, help="World directory")
	return parser


def main(args):

	type = HSAType.parse(args.type)
	dimension = Dimension.parse(args.dimension)

	startXChunk = args.startX // CHUNKSIZE
	startZChunk = args.startZ // CHUNKSIZE

	endXChunk = args.endX // CHUNKSIZE
	endZChunk = args.endZ // CHUNKSIZE

	box = Rectangle(args.startX, args.startZ, args.endX, args.endZ)

	if args.world.endswith('db'):
		world = args.world
	else :
		world = os.path.join(args.world, 'db')

	with leveldb.DB(world) as db :
		for x in range(startXChunk, endXChunk+1):
			for z in range(startZChunk,endZChunk+1):
				chunk = Rectangle(x*CHUNKSIZE, z*CHUNKSIZE, (x+1)*CHUNKSIZE-1, (z+1)*CHUNKSIZE-1)
				print("Modifying chunk x:%s, z:%s"%(x, z))
				intersect = box.intersection(chunk)
				
				key = Key( x, z, dimension.value if dimension != Dimension.OVERWORLD else None, HSATAG)
				bytesKey = key.toBytes()
				hsa = HSA(Position(intersect.x, args.startY, intersect.y, dimension.value), 
					Position(intersect.x1, args.endY, intersect.y1, dimension.value),
					type)
				print(hsa)

				alreayData = db.get(bytesKey)
				if alreayData is None :
					data = (1).to_bytes(4,"little")
					data += hsa.toBytes()
				else :
					amount = int.from_bytes(alreadyData[0:4],"little")
					data = (amount+1).to_bytes(4,"little") 
					data += alreayData[4:]
					data += hsa.toBytes()
				db.put(bytesKey, data)

if __name__ == '__main__' :
	parser = getArgParser()
	args = parser.parse_args()
	print(args) 
	
	setLdb(args.lib)
	main(args)
