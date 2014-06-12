#  libkarten.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import animations
import pygame
import os
import xml.etree.cElementTree as ET

class TileTemplate(object):
	def __init__(self,animation,play_anim=None,start_state="off"):
		self.animation=animation
		self.image=self.animation.states[list(self.animation.states.keys())[0]][0]
		self.rect=self.image.get_rect()
		self.frame=0
		self.state=start_state
class XMLTileSet(object):
	def __init__(self,folder_name):
		print("[libkarten]Initializing XMLTileSet class for "+str(folder_name)+".")
		self.tiles=[]
		self.path_from_here = os.path.join(folder_name)
		print("[libkarten]Initializing cElementTree for reading of XML animation data.")
		self.xml_tree = ET.parse(os.path.join(self.path_from_here,"tileset.xml"))
		self.xml_tree_root = self.xml_tree.getroot()
		for tile in self.xml_tree_root.findall("tile"):
			print("[libkarten]Reading tile data from XML:"+str(tile)+".")
			if int(tile.get("play"))==0:
				playanim=False
			else:
				playanim=True
			self.tiles.append(TileTemplate(animations.XMLTileAnimation(folder_name,tile.get("anim")),play_anim=playanim,start_state="off"))
		self.xml_tree=None
		self.xml_tree_root=None
		print(self.tiles)
class Tile(pygame.sprite.Sprite):
	def __init__(self,tiletemplate,layer,pos,collision_layers=[]):
		super(Tile,self).__init__()
		self.add(layer)
		self.c_layers=collision_layers
		self.animation=tiletemplate.animation
		self.image=tiletemplate.image
		self.rect=self.image.get_rect()
		self.frame=0
		for c_layer in self.c_layers:
			c_layer.append(self)
		self.state=tiletemplate.state
		self.playing=tiletemplate.playing
		self.rect.x=pos[0]
		self.rect.y=pos[1]
	def update_tile(self,delta):
		self.image=self.animation.get_frame(self.state,self.frame)
		self.rect=self.image.get_rect
		if self.playing:
			self.frame+=1
		if self.frame==len(self.animation.states[self.state])-1:
			self.frame=0
	def play(self):
		self.playing=True
	def stop(self):
		self.playing=False
		self.frame=0
	def pause(self):
		self.playing=False
	def set_state(self,state):
		self.state=state
	def tile_kill(self):
		for c_layer in self.c_layers:
			c_layer.remove(self)
		self.kill()
		del self
	def get_collide_layers(self):
		return self.c_layers
class Karte(object):
	def __init__(self):
		self.tiles=[]
		self.tilesets={}
		self.name=""
	def fromxml(self,map_name):
		tmptiles=[]
		self.name=map_name
		print("[libkarten]Loading Karte xml mapfile from map directory with name "+str(path)+".")
		path_to_mapfile=os.path.join("..","media","maps_xml",path,".xml")
		xml_tree = ET.parse(path_to_mapfile)
		xml_tree_root = xml_tree.getroot()
		tileset_defs_tag=root.findall("tileset_definitions")[0]
		for adding_tileset in tileset_defs_tag.findall("tileset"):
			self.tilesets[adding_tileset.get("name")]=XMLTileSet(adding_tileset.get("name"))
		tilestag=root.findall("map_tiles")[0]
		for tiles in tilestag.findall("tile"):
			c_layers=[]
			layer_temp=layers_l[int(tiles.get("layer")[6])]
			for col_layer in tiles.get("collision_layers").split():
				c_layers_temp.append(collisions_l[int(col_layer[6])])
			tmptiles.append(Tile(self.tilesets[tiles.get("tileset")][int(tiles.get("index"))],layer_temp,(tiles.get(pos).split()[0],tiles.get(pos).split()[1]),c_layers_temp))
	def update(self,delta):
		for tile in self.tiles:
			tile.update(delta)
	def kill_tile(self,tileref):
		tileref.tile_kill()
		self.tiles.remove(tileref)		
	def add_tile(self,tile_template,layer,pos,collision_layers=[]):
		tile_addition=Tile(tile_template,layer,pos,collision_layers)
		self.tiles.append(tile_addition)
	def get_tile_template(self,tileset_name,index):
		return tilesets[tileset_name].tiles[index]
	def uninitialize(self,reference):
		for tile in self.tiles:
			tile.tile_kill()
			del tile
		self.tiles=None
		self.tilesets=None
		self.name=None
		reference=None
		self=None
	def get_tiles_at_pos(self,pos):
		tmp=[]
		for tile in self.tiles:
			if tile.rect.collidepoint(pos):
				tmp.append(tile)
		return tmp
	def load_tileset(self,tset_name):
		self.tilesets[tset_name]=XMLTileSet(tset_name)
	def remove_tileset(self,tset_name):
		#this will not delete current tiles from that tileset
		self.tilesets[tset_name]=None
				
				
			
		
	

		
		
	

