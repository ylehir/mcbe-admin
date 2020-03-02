

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
