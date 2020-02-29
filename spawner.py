import sys
from hsa import Position
from multiprocessing import Pool

SPAWNERRANGE=16

def analyzeCluster(cluster):
	minX = []
	maxX = []
	minY = []
	maxY = []
	minZ = []
	maxZ = []
	dimension = 0
	for spawner in cluster :
		dimension = spawner.dimension
		minX.append(spawner.x - SPAWNERRANGE)
		maxX.append(spawner.x + SPAWNERRANGE)
		minY.append(spawner.y - SPAWNERRANGE)
		maxY.append(spawner.y + SPAWNERRANGE)
		minZ.append(spawner.z - SPAWNERRANGE)
		maxZ.append(spawner.z + SPAWNERRANGE)

	if len(cluster) == 2 :
		minX = max(minX)
		minY = max(minY)
		minZ = max(minZ)

		maxX = min(maxX)
		maxY = min(maxY)
		maxZ = min(maxZ)
	else:
		minX = min(minX)
		minY = min(minY)
		minZ = min(minZ)

		maxX = max(maxX)
		maxY = max(maxY)
		maxZ = max(maxZ)


	# scan all the spots !
	inRange = {}
	done = False
	for x in range(minX,maxX):
		for y in range(minY, maxY):
			for z in range(minZ, maxZ):
				pos = Position(x,y,z,dimension)
				inRange[pos] = set()
				for spawner in cluster :
					if pos.distance(spawner) <= SPAWNERRANGE :
						inRange[pos].add(spawner)
						if len(inRange[pos]) == len(cluster):
							done = pos
							break
				if done:
					break
			if done :
				break
		if done :
			break
	if done :
		if len(inRange[done]) == 0 :
			print(minX,maxX, minY, maxY, minZ, maxZ, cluster)
		return done, inRange[done]
	else :
		pos, s = sorted(inRange.items(), key = lambda i : len(i[1]), reverse=True)[0]
		if len(s) == 0 :
			print(minX,maxX, minY, maxY, minZ, maxZ, cluster)

		return pos,s

def findSpawners(spawners, nbProcess):
	print("Finding spawner clusters")
	clusters = set()
	posList = list(spawners.keys())
	for i, pos in enumerate(spawners.keys()) :
		cluster = [pos]
		for j in range(i, len(spawners)) :
			pos2 = posList[j]
			if pos != pos2 and pos.distance(pos2) < (SPAWNERRANGE*2) :
				cluster.append(pos2)
		if len(cluster) > 1 :
			clusters.add(tuple(sorted(cluster)))
	print("Analyzing clusters")
	with Pool(nbProcess) as p :
#	analyzed = []
#	for cluster in clusters :
#		analyzed.append(analyzeCluster(cluster))
		analyzed = p.map(analyzeCluster, clusters)
		for cluster in sorted(analyzed, key=lambda x : len(x[1]), reverse=True):
			afkPos, realCluster = cluster
			print("******* New cluster (%d) *******"%(len(realCluster)))
			for spawnerPos in realCluster :
				try :
					print(spawnerPos, spawners[spawnerPos]['EntityIdentifier'])
				except KeyError :
					print(spawnerPos, "Undefined")
			print("Afk spot : ", afkPos)

