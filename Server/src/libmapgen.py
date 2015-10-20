#  libmapgen.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

class MapGenerator(object):
	def __init__(self,ref_dict,tset,mapvar):
		self.mapvar=mapvar
		self.reference_table=ref_dict
		self.tileset_name=tset
		self.tiles_hashtab={}
		self.mapvar.load_tileset(tset)
		self.tiles_hashtab[(0,0)]=self.reference_table['base']
		self.maxx=50*32
		self.maxy=50*32
		for x in range(50):
			for y in range(50):
				self.tiles_hashtab[(x*32,y*32)]=self.reference_table['base']
	def add_to_map(self):
		for m,z in enumerate(self.tiles_hashtab.items()):
			x,y=z
			print('Calcing item %s/%s' % (str(m+1),len(self.tiles_hashtab.items())))
			self.mapvar.add_tile(self.mapvar.tilesets[self.tileset_name].tiles[y],self.mapvar.layers_l[3],3,x,'3',[self.mapvar.collisions_l[2]])
		self.mapvar.maxx=self.maxx
		self.mapvar.maxy=self.maxy
