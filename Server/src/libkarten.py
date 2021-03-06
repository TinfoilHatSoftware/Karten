#  libkarten.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import animations
import threading
import daswesen
import pygame
import os
import xml.etree.cElementTree as ET

	

class TileTemplate(object):
	def __init__(self, animation, tileset_name, index, start_state="off", play_anim=None):
		self.tileset_name = tileset_name
		self.index = index
		self.animation = animation
		self.image = self.animation.states[list(self.animation.states.keys())[0]][0]
		self.rect = self.image.get_rect()
		self.frame = 0
		self.state = start_state

class XMLTileSet(object):
	def __init__(self,folder_name):
		#print("[libkarten]Initializing XMLTileSet class for "+str(folder_name)+".")
		self.tiles=[]
		self.path_from_here = os.path.join("..","media","images","tiles",folder_name)
		#print("[libkarten]Initializing cElementTree for reading of XML animation data.")
		self.xml_tree = ET.parse(os.path.join(self.path_from_here,"tileset.xml"))
		self.xml_tree_root = self.xml_tree.getroot()
		for tile in self.xml_tree_root.findall("tile"):
		#	print("[libkarten]Reading tile data from XML:"+str(tile)+".")
			if int(tile.get("play"))==0:
				playanim=False
			else:
				playanim=True
			self.tiles.append(TileTemplate(animations.XMLTileAnimation(folder_name,tile.get("anim")),folder_name,tile.get("index"),start_state="off",play_anim=playanim))
		self.xml_tree=None
		self.xml_tree_root=None
		#print(self.tiles)
class Tile(pygame.sprite.Sprite):
	def __init__(self, tiletemplate, layer, layer_index, pos, collision_layer_indexes, collision_layers=[],origin=None):
		super(Tile, self).__init__()
		self.add(layer)
		self.c_layer_indexes = collision_layer_indexes
		self.layer = layer
		self.l_index = layer_index
		self.index = tiletemplate.index
		self.tileset_name = tiletemplate.tileset_name
		self.c_layers = collision_layers
		self.animation = tiletemplate.animation
		self.image = tiletemplate.image
		self.rect = self.image.get_rect()
		self.frame = 0
		### Maybe use a list comprehension here? -B
		for c_layer in self.c_layers:
			c_layer.append(self)
		self.state = tiletemplate.state
		self.playing = False
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		#print(self.c_layers)
	def update_tile(self, delta):
		self.image = self.animation.get_frame(self.state, self.frame)
		self.rect = self.image.get_rect
		if self.playing:
			self.frame += 1
		if self.frame == len(self.animation.states[self.state]) - 1:
			self.frame = 0
	def play(self):
		self.playing = True
	def stop(self):
		self.playing = False
		self.frame = 0
	def pause(self):
		self.playing = False
	def set_state(self, state):
		self.state = state
	def tile_kill(self):
		for c_layer in self.c_layers:
			c_layer.remove(self)
		self.kill()
		### del self won't work like you think it does -B
		del self
	def get_collide_layers(self):
		return self.c_layers

class Karte(object):
	def __init__(self, layers_l, collisions_l, update_reqs):
		self.reqs_update = update_reqs
		self.collisions_l = collisions_l
		self.layers_l = layers_l
		self.tiles = []
		self.tilesets = {}
		self.name = ""
	def fromxml(self, map_name, sender):
		tmptiles = []
		self.name = map_name
		#print("[libkarten]Loading Karte xml mapfile with name "+str(map_name)+".")
		path_to_mapfile = os.path.join("..", "media", "maps_xml", map_name + ".xml")
		try:
			xml_tree = ET.parse(path_to_mapfile)
		except IOError as e: return
		root = xml_tree.getroot()
		tileset_defs_tag = root.findall("tileset_definitions")[0]
		for adding_tileset in tileset_defs_tag.findall("tileset"):
			self.tilesets[adding_tileset.get("name")]=XMLTileSet(adding_tileset.get("name"))
		tilestag = root.findall("map_tiles")[0]
		for tiles in tilestag.findall("tile"):
			layer_temp = self.layers_l[int(tiles.get("layer")) - 1]
			c_layers_temp = []
			c_indexes_temp = ""
			for col_layer in tiles.get("collision_layers").split():
				c_layers_temp.append(self.collisions_l[int(col_layer) - 1])
			c_indexes_temp = tiles.get("collision_layers")
			self.tiles.append(Tile(self.tilesets[tiles.get("tileset")].tiles[int(tiles.get("index"))], layer_temp,int(tiles.get("layer")), (int(tiles.get("pos").split()[0]), int(tiles.get("pos").split()[1])), c_indexes_temp, c_layers_temp))
		entstag = root.findall("ents")[0]
		for ent in entstag.findall("ent"):
			self.tiles.append(daswesen.load_wesen(ent.get("entfile"), (int(ent.get("pos").split()[0]), int(ent.get("pos").split()[1])), self.layers_l, self.collisions_l, self.reqs_update, sender))
			self.tilesets[ent.get("entfile").replace(".py","")]=EntTilesetMockup(ent.get("entfile"))
	def update(self,delta):
		for tile in self.tiles:
			tile.update(delta)
	def kill_tile(self,tileref):
		tileref.tile_kill()
		self.tiles.remove(tileref)
	def add_tile(self, tile_template, layer, layer_index, pos, col_indexes, collision_layers=[]):
		tile_addition = Tile(tile_template, layer, layer_index, pos, col_indexes, collision_layers)
		for c in col_indexes.split():
			self.collisions_l[int(c)].append(tile_addition)
		#print(self.collisions_l)
		self.tiles.append(tile_addition)
	def get_tile_template(self, tileset_name, index):
		return self.tilesets[tileset_name].tiles[index]
	def uninitialize(self,reference):
		for tile in self.tiles:
			tile.tile_kill()
			del tile
		self.tiles = None
		self.tilesets = None
		self.name = None
		reference = None
		### Again, this may not work like you think it does -B
		self = None
	def get_tiles_at_pos(self, pos):
		tmp = []
		for tile in self.tiles:
			if tile.rect.collidepoint(pos):
				tmp.append(tile)
		return tmp
	def load_entdef(self, entname):
		self.tilesets[entname.replace(".py","")] = EntTilesetMockup(entname)
	def load_tileset(self, tset_name):
		self.tilesets[tset_name] = XMLTileSet(tset_name)
	def remove_tileset(self,tset_name):
		#this will not delete current tiles from that tileset
		del self.tilesets[tset_name]
	def get_tiles_from_tileset(self, tset_name):
		return self.tilesets[tset_name].tiles
	def get_all_tiles(self):
		return self.tiles
	def get_tilesets_dict(self):
		return self.tilesets
	def remove_rect(self,rect):
		count=0
		for tile in self.tiles:
			if tile.rect.colliderect(rect):
				count+=1
				tile.tile_kill()
				self.tiles.remove(tile)
		#print('COUNT IS HEREEEEEEEEEEe:',count)
	def make_xml(self):
		tsetdefs = []
		tiledefs = []
		entdefs = []
		root = ET.Element("karte")
		tset_defs = ET.SubElement(root, "tileset_definitions")
		for tset_name,tset in self.tilesets.items():
			is_wesen_tset = True
			try:
				tset.is_wesen_mockup
			except:
				is_wesen_tset = False
			if not is_wesen_tset:
				tsetdefs.append(ET.SubElement(tset_defs, "tileset", name=tset_name))
		tile_defs = ET.SubElement(root, "map_tiles")
		ent_defs = ET.SubElement(root, "ents")
		for tile in self.tiles:
			iswesen = True
			try:
				tile.is_wesen
			except:
				iswesen = False
			if iswesen == True:
				entdefs.append(ET.SubElement(ent_defs, "ent", entfile=tile.name, pos=str(tile.rect.x) + " " + str(tile.rect.y)))
			else:
				tiledefs.append(ET.SubElement(tile_defs, "tile", tileset = tile.tileset_name, index=tile.index, pos=str(tile.rect.x) + " " + str(tile.rect.y), layer=str(tile.l_index), collision_layers = tile.c_layer_indexes))
			iswesen = None
		return ET.tostring(root)
	def loadWesenWithID(self, ent, pos, reqs_update, owner, sender, ent_id=None):
		print('InWesenID: %s' % str(owner))
		if ent_id is not None:
			ent = daswesen.load_wesen(ent, pos, self.layers_l, self.collisions_l, reqs_update, sender, ent_id)
			ent.owner = owner
		else:
			ent = daswesen.load_wesen(ent, pos, self.layers_l, self.collisions_l, reqs_update, sender)
			ent.owner = owner
		self.tiles.append(ent)
		try:
			ent.go()
		except:	pass

class EntTilesetMockup(object):
	def __init__(self, ent_name):
		ent = daswesen.load_wesen_constructor(ent_name)
		self.thumb = pygame.image.load(os.path.join("entities", "thumbs", ent_name + ".png"))
		self.tiles = []
		self.name = ent_name
		self.tiles.append(ent)
		self.is_wesen_mockup = True

