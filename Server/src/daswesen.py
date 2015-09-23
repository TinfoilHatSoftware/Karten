#  daswesen.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
import pygame
import imp
import animations
import libkarten
import os
class GrafikWesenBase(pygame.sprite.Sprite):
	def __init__(self,animation,positionxy,collision_layers,collision_layers_index,draw_layer,draw_layer_index,initial_graphic_state):
		super(GrafikWesenBase,self).__init__()
		self.animation=animation
		self.image=self.animation.get_frame(initial_graphic_state[0],initial_graphic_state[1])
		self.c_layer_indexes=collision_layers_index
		self.rect=self.image.get_rect()
		try:
			self.add(self.layer)
		except:
			pass
		self.l_index=draw_layer_index
		self.state=initial_graphic_state[0]
		self.frame=initial_graphic_state[1]
		self.c_layers=collision_layers
		try:
			for c_layer in self.c_layers:
				c_layer.append(self)
		except:	pass
		self.rect.x=positionxy[0]
		self.rect.y=positionxy[1]
		self.is_wesen=True
	def set_state_and_frame(self,state_name,frame_int):
		self.image=self.animation.get_frame(state_name,frame_int)
	def tile_kill(self):
		for c_layer in self.c_layers:
			c_layer.remove(self)
		self.kill()
		del self
	def get_collide_layers(self):
		return self.c_layers
	def get_rect(self):
		return self.rect
	def set_rect(self,rect):
		self.rect=rect

def get_ent_directives(entname):
	directive_start_line=-100
	directive_end_line=-100
	directives_thing=[]
	f=open(os.path.join("..","src","entities",entname+".py"),"r+")
	f.seek(0)
	for lineno,line in enumerate(f):
		if "#BEGIN DIRECTIVES" in line:
			directive_start_line=lineno+1
		if "#END DIRECTIVES" in line:
			directive_end_line=lineno+1
	if directive_end_line==-100 or directive_start_line==-100:
		return None
	f.seek(0)
	for lineno,line in enumerate(f):
		line=line.strip("\n")
		if "#DIRECTIVE" in line:
			directives_thing.append((line.strip("\n").split()[1],line.strip("\n").split()[2]))
	f.close()
	#print(directives_thing)
	return directives_thing

def load_wesen(wesen_name,position,layers_list,collision_layers_list,reqs_update_var_thing,root,ent_id=None):
	directives=get_ent_directives(wesen_name)
	loaderargs=[]
	reqs_update_var=False
	for directive_name,directive_value in directives:
		if directive_name=="ANIMATION":
			loaderargs.append(animations.XMLAnimation(directive_value))
		if directive_name=="POSITION":
			loaderargs.append(position)
		if directive_name=="LAYER":
			loaderargs.append((int(directive_value)-1,layers_list[int(directive_value)-1]))

		if directive_name=="COLLISION_LAYERS":
			col_layers=[]
			for col_layer_num in directive_value.split("_"):
				col_layers.append(collision_layers_list[int(col_layer_num)-1])
			loaderargs.append((directive_value.replace("_"," "),col_layers))
		if directive_name=="REQS_UPDATE":
			reqs_update_var=True
	module = imp.load_source(wesen_name, os.path.join("entities",wesen_name+".py"))
	ent=module.WesenEnt(*loaderargs)
	ent.data='000'
	if reqs_update_var:
		reqs_update_var_thing.append(ent)
	if ent_id!=None:
		root.add_ent_id_ref(ent,ent_id)
	else:
		root.add_ent_id_ref(ent)
	return ent
def load_wesen_constructor(wesen_name):
	module = imp.load_source(wesen_name, os.path.join("entities",wesen_name+".py"))
	return module
		
				
			
		
		
	
