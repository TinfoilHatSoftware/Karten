#  conversionist.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import pickle
import daswesen
n='[library conversionist]'

def convertMap(mapx):
	all_tiles=[]
	tilesets=[]
	mapx=mapx.c_map
	for key,value in mapx.tilesets.items():
		mockup=True
		try:
			value.is_wesen_mockup
		except:
			mockup=False
		tilesets.append((mockup,key))
	for tile in mapx.tiles:
		iswesen=True
		try:
			tile.is_wesen
		except:
			iswesen=False
		if iswesen:
			#print(tile.name)
			tile.index=0
			tile.tileset_name=tile.name
			ent_id=tile.id
		else:
			ent_id=0
		try:
			tile.owner
		except:
			tile.owner=None
		all_tiles.append((iswesen,tile.tileset_name,tile.l_index,tile.c_layer_indexes,tile.index,tile.rect.x,tile.rect.y,ent_id,tile.owner))
	bytes_data=pickle.dumps((all_tiles,tilesets))
	return bytes_data
def reverseConvertMap(data,mapobj,sender):
	data=pickle.loads(data)
	print(data)
	tiles=data[0]
	tilesets=data[1]
	for tileset in tilesets:
		is_mockup,name=tileset
		if not is_mockup:
			mapobj.load_tileset(name)
		else:
			mapobj.load_entdef(name)
	for tile in tiles:
		iswesen,tilesetname,layerindex,clayerindexes,tileindex,tilex,tiley,ent_id,owner=tile
		if not iswesen:
			clayers=[]
			for index in clayerindexes:
				clayers.append(mapobj.collisions_l[int(index)-1])
			mapobj.add_tile(mapobj.tilesets[tilesetname].tiles[int(tileindex)],mapobj.layers_l[int(layerindex)-1],layerindex,(int(tilex),int(tiley)),clayerindexes,clayers)
		else:
			ent=daswesen.load_wesen(tilesetname,(int(tilex),int(tiley)),mapobj.layers_l,mapobj.collisions_l,mapobj.reqs_update,sender,ent_id)
			if owner!=None:
				ent.owner=owner
			mapobj.tiles.append(ent)





