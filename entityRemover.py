
import io
import nbt

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

