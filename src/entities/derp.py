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
		explode_sound=pygame.mixer.Sound(join('..','media','sound','explode.wav'))
		blast_sound=pygame.mixer.Sound(join('..','media','sound','blast.wav'))
		self.sounds=(explode_sound,blast_sound)
		self.projectile_anims=(animations.XMLAnimation('blue_explosion'),animations.XMLAnimation('plasma_explosive_projectile'))
		self.missiles=[]
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		if self.going==True:
			if self.firsttime==True:
				sender.lock_camera_to_ent(self.get_ent_rect,self.set_self_rect)
				self.firsttime==False
				sender.charcont=self
			self.counter+=delta
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						if self.state=='left':
							y=0
							x=-1
						if self.state=='right':
							y=0
							x=1
						if self.state=='up':
							y=-1
							x=0
						if self.state=='down':
							y=1
							x=0
						projectiles.PlasmaExplosive(self.rect.center,(x,y),self.layer,self.c_layers[0],sender.reqs_update,self.projectile_anims,self.sounds)
			keys=pygame.key.get_pressed()
			if keys[pygame.K_a]:
				self.rect.x-=delta/4
				self.xvel=-1
				self.yvel=0
				self.state='left'
				self.moving=True
			elif keys[pygame.K_w]:
				self.rect.y-=delta/4
				self.yvel=-1
				self.xvel=0
				self.state='up'
				self.moving=True
			elif keys[pygame.K_s]:
				self.rect.y+=delta/4
				self.yvel=1
				self.xvel=0
				self.state='down'
				self.moving=True
			elif keys[pygame.K_d]:
				self.rect.x+=delta/4
				self.xvel=1
				self.yvel=0
				self.state='right'
				self.moving=True
			else:
				self.moving=False
				self.frame=0
				self.xvel=0
				self.yvel=0
				self.set_state_and_frame(self.state,self.frame)
			if self.counter>=100 and self.moving:
				self.counter=0
				if self.frame==len(self.animation.states[self.state])-1:
					self.frame=0
					self.set_state_and_frame(self.state,self.frame)
				else:
					self.frame+=1
					self.set_state_and_frame(self.state,self.frame)
			for wall in sender.c_map.tiles:	
				if self.rect.colliderect(wall.rect) and  self.c_layers[0] in wall.c_layers and wall!=self:
					if self.xvel > 0: # Moving right; Hit the left side of the wall
						self.rect.right = wall.rect.left
						print(self.rect.right,self.rect.left)
					if self.xvel < 0: # Moving left; Hit the right side of the wall
						self.rect.left = wall.rect.right
					if self.yvel > 0: # Moving down; Hit the top side of the wal
						self.rect.bottom = wall.rect.top
					if self.yvel < 0: # Moving up; Hit the bottom side of the wal
						self.rect.top = wall.rect.bottom
	def go(self):
		self.going=True
	def get_ent_rect(self):
		return self.rect
	def set_self_rect(self,rect):
		self.rect=rect
		
