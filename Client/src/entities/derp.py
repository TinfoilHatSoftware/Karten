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
#DIRECTIVE ANIMATION evil_robot_blue
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
		self.ent_id=0
		self.localplayerchar=True
		self.counter=0
		self.projectiles=[]
		self.xvel=0
		self.yvel=1
		self.frame=0
		self.going=False
		self.moving=False
		self.is_wesen=True
		self.firsttime=True
		self.framecounter=0
		self.energy=200
		self.health=200
		self.original_pos=position
		self.projectile_anims=(animations.XMLAnimation('blue_explosion'),animations.XMLAnimation('plasma_explosive_projectile'))
		self.missiles=[]
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		if self.going==True:
			if self.framecounter==50:
				self.framecounter=0
				if self.energy<200:
					self.energy+=10
			else:
				self.framecounter+=1
			if self.firsttime==True:
				sender.lock_camera_to_ent(self.get_ent_rect,self.set_self_rect)
				self.firsttime=False
				sender.charcont=self
				explode_sound=pygame.mixer.Sound(join('..','media','sound','explode.wav'))
				blast_sound=pygame.mixer.Sound(join('..','media','sound','blast.wav'))
				self.sounds=(explode_sound,blast_sound)
			self.counter+=delta
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and self.energy>=50:
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
						self.energy-=50
						self.projectiles.append(projectiles.PlasmaExplosive(self.rect.center,(x,y),sender.layer2,self.c_layers[0],sender.reqs_update,self.projectile_anims,self.sounds,self))
			keys=pygame.key.get_pressed()
			derp=False
			derp2=False
			if keys[pygame.K_a]:
				self.xvel=-1
				#self.yvel=0
				self.state='left'
				self.moving=True
			elif keys[pygame.K_d]:
				self.xvel=1
				#self.yvel=0
				self.state='right'
				self.moving=True
			else:
				derp=True
			if keys[pygame.K_w]:
				if self.bottomed:
					self.rect.y-=20
				self.moving=True
			else:
				derp2=True
			#elif keys[pygame.K_s]:
			#	self.rect.y+=delta/4
			#	self.yvel=1
			#	self.xvel=0
			#	self.state='down'
			#	self.moving=True
			if derp and derp2:
				self.moving=False
				self.frame=0
				self.xvel=0
				#self.yvel=0
				self.set_state_and_frame(self.state,self.frame)
			self.rect.x+=self.xvel*(delta/2)
			self.rect.y+=self.yvel*(delta)
			if self.counter>=100 and self.moving:
				self.counter=0
				if self.frame==len(self.animation.states[self.state])-1:
					self.frame=0
					self.set_state_and_frame(self.state,self.frame)
				else:
					self.frame+=1
					self.set_state_and_frame(self.state,self.frame)
			self.bottomed=False
			for sprite in pygame.sprite.spritecollide(self,self.c_layers[0],False):
				if sprite!=self and sprite not in self.projectiles:
					if self.xvel > 0: # Moving right; Hit the left side of the wall
						self.rect.right = sprite.rect.left
					elif self.xvel < 0: # Moving left; Hit the right side of the wall
						self.rect.left = sprite.rect.right
					elif self.yvel > 0: # Moving down; Hit the top side of the wal
						self.rect.bottom = sprite.rect.top
					elif self.yvel < 0: # Moving up; Hit the bottom side of the wal
						self.rect.top = sprite.rect.bottom
					self.grounded=False
					if sprite.rect.collidepoint(self.rect.centerx,self.rect.bottom+4):
						self.grounded=True
					if self.grounded==True:
						self.yvel=0
					else:
						self.yvel=1
			#for x in self.c_layers[0]:
				#pygame.draw.rect(sender.screen,(222,222,222),(x.rect.x+700,x.rect.y,x.rect.x+(x.rect.width+700),x.rect.y+(x.rect.height)),2)
	def go(self):
		self.going=True
	def get_ent_rect(self):
		return self.rect
	def set_self_rect(self,rect):
		self.rect=rect
		
