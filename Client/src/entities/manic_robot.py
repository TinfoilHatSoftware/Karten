#  Entity Defintion
#  
#  Copyright 2014 Jacob Swart
#
#  This entdef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
#
#
#DO NOT UNCOMMENT THE FOLLOWING LINES. They are directives to the entity loader and must remain commented to be effective.
#BEGIN DIRECTIVES
#DIRECTIVE ANIMATION mech_tan_resized
#DIRECTIVE POSITION ;
#DIRECTIVE LAYER 3
#DIRECTIVE COLLISION_LAYERS 3
#DIRECTIVE REQS_UPDATE ;
#END DIRECTIVES
import daswesen
import pygame
import animations
import projectiles
from os.path import join as join
def round32(x): return (x+0b10000) & (~0b11111)
class WesenEnt(daswesen.GrafikWesenBase):
	def __init__(self,animation,position,layer,collision_layers):
		self.layer=layer[1]
		self.name="manic_robot"
		self.localplayerchar=True
		self.counter=0
		self.xvel=0
		self.yvel=0
		self.frame=0
		self.going=False
		self.moving=False
		self.c_layers=collision_layers
		self.is_wesen=True
		self.firsttime=True
		self.framecounter=0
		self.exploded=False
		self.health=200
		self.projectile_anims=(animations.XMLAnimation('blue_explosion'),animations.XMLAnimation('plasma_explosive_projectile'))
		self.missiles=[]
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		if self.going==True:
			if self.firsttime==True:
				self.firsttime=False
				explode_sound=pygame.mixer.Sound(join('..','media','sound','explode.wav'))
				blast_sound=pygame.mixer.Sound(join('..','media','sound','blast.wav'))
				self.sounds=(explode_sound,blast_sound)
			if self.framecounter<2:
				self.framecounter+=1
			else:
				self.framecounter=0
				if round32(sender.charcont.rect.x)==round32(self.rect.x):
					projectiles.PlasmaExplosive(self.rect.center,(0,-1),sender.layer2,self.c_layers[0],sender.reqs_update,self.projectile_anims,self.sounds,self)
			self.state='up'
			self.set_state_and_frame(self.state,self.frame)
			if self.health<=0:
				self.kill()
				self.tile_kill()
				projectiles.Explosion(self.rect.center,self.layer,sender.reqs_update,self.projectile_anims[0],self,self.sounds[0])
				sender.c_map.tiles.remove(self)
				self.going=False
				for x in self.c_layers:
					x.remove(self)
				self.exploded=True
				del self
	def go(self):
		self.going=True
	def tile_kill(self):
		try:
			self.c_layer.remove(self)
		except: pass
		self.kill()
		del self
