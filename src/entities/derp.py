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
class WesenEnt(daswesen.GrafikWesenBase):
	def __init__(self,animation,position,layer,collision_layers):
		self.layer=layer[1]
		self.name="derp"
		self.localplayerchar=True
		self.counter=0
		self.xvel=0
		self.yvel=0
		self.frame=0
		self.going=False
		self.moving=False
		self.is_wesen=True
		self.firsttime=True
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		if self.going==True:
			if self.firsttime==True:
				sender.lock_camera_to_ent(self.get_ent_rect,self.set_self_rect)
				self.firsttime==False
			self.counter+=delta
			keys=pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				self.rect.x-=delta/4
				self.xvel=-1
				self.state='left'
				self.moving=True
			elif keys[pygame.K_UP]:
				self.rect.y-=delta/4
				self.yvel=-1
				self.state='up'
				self.moving=True
			elif keys[pygame.K_DOWN]:
				self.rect.y+=delta/4
				self.yvel=1
				self.state='down'
				self.moving=True
			elif keys[pygame.K_RIGHT]:
				self.rect.x+=delta/4
				self.xvel=1
				self.state='right'
				self.moving=True
			else:
				self.moving=False
				self.frame=0
				self.set_state_and_frame(self.state,self.frame)
			if self.counter>=100 and self.moving:
				self.counter=0
				if self.frame==len(self.animation.states[self.state])-1:
					self.frame=0
					self.set_state_and_frame(self.state,self.frame)
				else:
					self.frame+=1
					self.set_state_and_frame(self.state,self.frame)
	def go(self):
		self.going=True
	def get_ent_rect(self):
		return self.rect
	def set_self_rect(self,rect):
		self.rect=rect
		
