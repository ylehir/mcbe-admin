
import leveldb
import argparse
from leveldb import Row, setLdb, Key
from collections import namedtuple, defaultdict
from enum import Enum
from hsa import HSA,Position,HSAType
from spawner import findSpawners
import nbt
import io
import os
import sys
import datetime

CHUNKSIZE=16

def getArgParser():
	parser = argparse.ArgumentParser(description="Minecraft Bedrock admin toolkit")
	parser.add_argument("--nbProcess", type=int, default=12, help="Number of process used for analysis")
	parser.add_argument("--lib", type=str, help="Path to leveldb MCPE lib (dll or so file) (from https://github.com/Mojang/leveldb-mcpe)")
	parser.add_argument("world", type=str, help="World directory")
	parser.add_argument("--removeEntities", "-r", action="store_true", help="Remove non persistent entities.")
	parser.add_argument("--pendingTicks", "-p", action="store_true", help="Fix pending ticks.")
	parser.add_argument("--worldBorders", "-w", type=str, help="CSV File containing coords of world borders. (See README for syntax)")
	parser.add_argument("--findSpawners", "-f", action="store_true")
	parser.add_argument("--dumpHSA", "-d", action="store_true")
	parser.add_argument("--compact", "-c", action="store_true", help="Try to compact the db at the end.")
	return parser

class Borders(object):
	def __init__(self, borders):
		self._borders = borders

	def __contains__(self, coords):
		for border in self._borders :
			if coords in border:
				return True
				
class Border(object):
	def __init__(self, dimension, x, z, x1, z1):
		self.dimension = dimension
		if x > x1 :
			self.x  = x1 // CHUNKSIZE
			self.x1 = x  // CHUNKSIZE
		else :
			self.x  = x  // CHUNKSIZE
			self.x1 = x1 // CHUNKSIZE
		if z > z1 :
			self.z  = z1 // CHUNKSIZE
			self.z1 = z  // CHUNKSIZE
		else :
			self.z  = z  // CHUNKSIZE
			self.z1 = z1 // CHUNKSIZE

	def __str__(self):
		return "d : %s, x : %s z : %s, x1 : %s z1 : %s"%(self.dimension, self.x, self.z, self.x1, self.z1)

	def __contains__(self, coords):
		dimension,x,z = coords
		return dimension == self.dimension and x >= self.x and x <= self.x1 and z >= self.z and z <= self.z1

entitiesFiler=( "+minecraft:drowned"
		,   "+minecraft:guardian"
		,   "+minecraft:magma_cube"
		,   "+minecraft:silverfish"
		,   "+minecraft:skeleton"
		,   "+minecraft:slime"
		,   "+minecraft:stray"
		,   "+minecraft:witch"
		,	"+minecraft:zombie"
		,	"+minecraft:zombie_pigman"
		,	"+minecraft:zombie_villager_v2")

def filterEntities(value, args):
	buff = io.BytesIO(value)
	outBuff = io.BytesIO()
	removed=False
	while True :
		try :
			tree = nbt.NBTFile(buffer=buff)
			try :
				name = tree['CustomName']
				tree.write_file(buffer=outBuff)
			except KeyError:
				try :
					if tree['IsTamed'] :
						tree.write_file(buffer=outBuff)
					elif "+minecraft:charged_creeper" in tree["definitions"]:
						tree.write_file(buffer=outBuff)
					elif not tree["NaturalSpawn"] :
						found = False
						for definition in tree['definitions'] :
							if definition in entitiesFiler :
								removed = True
								found = True
								break
						if not found :
							tree.write_file(buffer=outBuff)
					else:
						removed = True
				except KeyError as e :
					tree.write_file(buffer=outBuff)
		except nbt.MalformedFileError:
			break
	if removed :
		return outBuff
	else :
		return None

def fixPendingTicks(key, value, args):
	buff = io.BytesIO(value)
	outBuff = io.BytesIO()
	modified = 0
	while True :
		try :
			tree = nbt.NBTFile(buffer=buff)
			try :
				if tree['tickList']:
					modified += 1
					newList = nbt.TAG_List(type=nbt.TAG_Compound, name='tickList')
					tree['tickList'] = newList
					tree.write_file(buffer=outBuff)
			except KeyError:
				pass
		except nbt.MalformedFileError:
			break
	return modified, outBuff

def getWorldBordersFromFile(worldBorderFile):
	borders = []
	with open(worldBorderFile, 'r') as fd :
		for line in fd :
			splits = line.split(',')
			if len(splits) == 5 :
				dimension,x,z,x1,z1 = splits
			elif len(splits) == 1 :
				dimension = splits[0]
				x = -sys.maxsize
				z = -sys.maxsize
				x1 = sys.maxsize
				z1 = sys.maxsize
			border = Border(int(dimension),int(x), int(z), int(x1), int(z1))
			borders.append(border)
	return Borders(borders)

	
def main(args):
	date = datetime.datetime.now()
	worldBorders = []
	if args.worldBorders :
		worldBorders = getWorldBordersFromFile(args.worldBorders)
	world = ""
	if args.world.endswith('db'):
		world = args.world
	else :
		world = os.path.join(args.world, 'db')
	
	spawners = {}
	ships = {}
	with leveldb.DB(world) as db :
		if args.worldBorders or args.removeEntities or args.pendingTicks or args.dumpHSA or args.findSpawners or args.compact:
			print("Reading database")
			for entry in db:
				if not  isinstance(entry, Row):
					print(entry)
					continue
				key = Key.fromBytes(entry.key)
				if not key :
					continue
#				if args.compact and key.tag not in (45,46,47,48,49,50,51,52,53,54,118):
#					db.delete(entry.key)
				if args.worldBorders and (key.dimension, key.x, key.z) not in worldBorders:
					print("Removing d:%s x:%s z:%s"%( key.dimension, key.x, key.z))
					db.delete(entry.key)
					continue
				if key.tag == 50 and args.removeEntities :
					outBuff = filterEntities(entry.value, args)
					if outBuff :
						db.put(entry.key, outBuff.getvalue())
				elif key.tag == 51 and args.pendingTicks:
					removed, outBuff = fixPendingTicks(key, entry.value, args)
					if removed:
						print("Removed %d pendingTicks in d:%s, x:%s, z:%s"%( removed, key.dimension, key.x, key.z))
						db.put(entry.key, outBuff.getvalue())
				elif key.tag == 49 and args.findSpawners:
					buff = io.BytesIO(entry.value)
					if entry.value :
						tree = nbt.NBTFile(buffer=buff)
						if tree['id'] == "MobSpawner":
							spawners[Position(tree['x'].value, tree['y'].value, tree['z'].value, key.dimension)] = tree
				elif key.tag == 57 and (args.dumpHSA or args.compact):
					amount = int.from_bytes(entry.value[0:4],"little")
#					newAmount = 0
#					newData = b""
					for x in range(amount):
						hsa = HSA.fromBytes(entry.value[x*25+4:(x+1)*25+4], key.dimension)
						print(hsa)
#				elif key.tag == 47 and args.compact :
#						palette = { 0x2 : (32,1,False) , 0x4 : (16,2,False), 0x6 : (10,3,True) , 0x8 : (8,4,False) , 0xa : (6,5,True) , 0xc: (5,6,True) , 0x10: (4,8,False) , 0x20 : (2,16,False) }
#						pal = int(entry.value[2])
#						chunkPalFormat = palette[pal]
#						size = len(entry.value)
#						end = (4096//chunkPalFormat[0])*4 + int(chunkPalFormat[2])*4
#				#                   print(key, len(entry.value), pal, chunkPalFormat, end+7)
#						buff = io.BytesIO(entry.value[end+7:])
#						chunkPalette = []
#						while True :
#							try :
#								tree = nbt.NBTFile(buffer=buff)
#				#                           print(tree.pretty_tree())
#								chunkPalette.append(tree)
#							except nbt.MalformedFileError:
#								break
#						data = entry.value[3:end]
#						usedId = set()
#						for index in range(0,end,4):
#							value = int.from_bytes(data[index:index+3], byteorder="big")
#							for blockId in range(0,32, chunkPalFormat[1]):
#								blockVal = (value >> blockId) & ((1<<chunkPalFormat[1])-1)
#				#                           print(blockId, blockVal, chunkPalette[blockVal]["name"])
#						usedId.add(blockVal)
#						if len(usedId) > len(chunkPalette):
#							print(key, len(entry.value), pal, chunkPalFormat, end+7)
#							print(usedId, len(chunkPalette), int.from_bytes(entry.value[end+3:end+7], "little"))

		if args.compact:
			db.compactRange(None,0,None,0)
	
	if args.findSpawners:
#		for x in sorted(ships.keys()): 
#			print("%s : x : %s, y: %s, z: %s"%(ships[x], x[0], x[2], x[1]))		
		findSpawners(spawners, args.nbProcess)

if __name__ == '__main__' :
	parser = getArgParser()
	args = parser.parse_args()
	setLdb(args.lib)
	main(args)
