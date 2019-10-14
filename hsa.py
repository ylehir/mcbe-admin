
from enum import Enum
import struct

class Rectangle(object):
	def __init__(self, x, y, x1, y1):
		if x>x1 or y>y1:
			raise ValueError("Coordinates are invalid")
		self.x = x
		self.y = y
		self.x1 = x1
		self.y1 = y1

	def intersection(self, other):
		a, b = self, other
		x  = max(min(a.x, a.x1), min(b.x, b.x1))
		y  = max(min(a.y, a.y1), min(b.y, b.y1))
		x1 = min(max(a.x, a.x1), max(b.x, b.x1))
		y1 = min(max(a.y, a.y1), max(b.y, b.y1))
		if x<x1 and y<y1:
			return Rectangle(x, y, x1, y1)
	__and__ = intersection

	def __repr__(self):
		return "Rectangle : x: %s y: %s x1: %s y1: %s"%(self.x, self.y, self.x1, self.y1)


class Position(object):
	def __init__(self, x, y, z, dimension):
		self.x = x
		self.y = y
		self.z = z
		self.dimension = dimension

	def __hash__(self):
		return hash((self.x,self.y,self.z))

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "(d:%s, x:%s, y:%s, z:%s)"%(self.dimension, self.x, self.y, self.z)

	def __eq__(self, pos):
		return self.dimension == pos.dimension and self.x == pos.x and self.y == pos.y and self.z == pos.z

	def distance(self, pos):
		if self.dimension != pos.dimension :
			return sys.maxsize
		return abs(self.x - pos.x) + abs(self.y - pos.y) + abs(self.z - pos.z)

class Dimension(Enum):
	OVERWORLD=0
	NETHER=1
	END=2
	
	@classmethod
	def parse(cls, value):
		if value =="overworld" : 
			value = 0
		elif value=="nether":
			value=1
		elif value=="end":
			value=2
		else:
			raise NotImplementedError("Unknonw dimension : %s"%value)
		return Dimension(value)

class HSAType(Enum):
	FORTRESS=1
	HUT=2
	MONUMENT=3
	UNKNOWN=4
	OUTPOST=5
	UNKNOWN=6

	@classmethod
	def parse(cls, value):
		if value =="fortress":
			value=1
		elif value=="hut":
			value=2
		elif value=="monument":
			value=3
		elif value=="outpost":
			value=5
		else :
			raise NotImplementedError("Unknonw structure : %s"%value)
		return HSAType(value)
	
class HSA(object):

	def __init__(self, pos1, pos2 , type):
		self.pos1 = pos1 
		self.pos2 = pos2
		self.type = type
	
	@staticmethod
	def fromBytes(bytes, dimension):
		data = struct.unpack("<iiiiiib",bytes)
		pos1 = Position(data[0], data[1], data[2], dimension)
		pos2 = Position(data[3], data[4], data[5], dimension)
		type = HSAType(data[6])
		return HSA(pos1, pos2, type)

	def toBytes(self):
		return struct.pack("<iiiiiib", self.pos1.x, self.pos1.y, self.pos1.z
							  		 , self.pos2.x, self.pos2.y, self.pos2.z
								     , self.type.value)

	def __repr__(self):
		return str(self)
		
	def __str__(self):
		return "Type : %s %s -> %s"%(self.type, self.pos1, self.pos2)
