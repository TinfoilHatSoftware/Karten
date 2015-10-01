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
		self.yvel=0
		self.move_speed=50
		self.max_gravity=100
		self.jump_speed=100
		self.frame=0
		self.is_grounded=False
		self.going=False
		self.is_wesen=True
		self.firsttime=True
		self.framecounter=0
		self.energy=200
		self.health=200
		self.owner=0
		self.data='0'
		self.original_pos=position
		self.projectile_anims=(animations.XMLAnimation('blue_explosion'),animations.XMLAnimation('plasma_explosive_projectile'))
		self.missiles=[]
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		#print(self.data)
		inputx=[]
		inputy=''
		try:
			inputx=sender.input[self.owner].split()
		except:
			pass
		try:
			inputy=sender.input[self.owner]
		except:
			pass
		#print(inputx)
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
							self.data+='0'
							y=0
							x=-1
						if self.state=='right':
							self.data+='1'
							y=0
							x=1
						if self.state=='up':
							self.data+='2'
							y=-1
							x=0
						if self.state=='down':
							self.data+='3'
							y=1
							x=0
						self.energy-=50
						self.projectiles.append(projectiles.PlasmaExplosive(self.rect.center,(x,y),sender.layer2,self.c_layers[0],sender.reqs_update,self.projectile_anims,self.sounds,self))
			keys=pygame.key.get_pressed()
			#print(self.data)
			try:
				m=inputy.split('*',1)[1]
				if int(m.split(' ')[0])>self.rect.x:
					self.state='right'
				else:
					self.state='left'
			except:
				pass
			if self.state=='left':
				self.data+='0'
			if self.state=='right':
				self.data+='1'
			if self.state=='up':
				self.data+='2'
			if self.state=='down':
				self.data+='3'
			derp=False
			
			derp2=False
			if 'a' in inputx:
				#self.yvel=0
				self.xvel=(-self.move_speed)
				#self.state='left'
				self.moving=True
			elif 'd' in inputx:
				self.xvel=self.move_speed
				#self.yvel=0
				#self.state='right'
				self.moving=True
			else:
				derp=True
			if 'w' in inputx:
				if self.is_grounded:
					self.yvel-=self.jump_speed
					self.is_grounded=False
			else:
				derp2=True
			self.is_grounded=False
			#elif keys[pygame.K_s]:
			#	self.rect.y+=delta/4
			#	self.yvel=1
			#	self.xvel=0
			#	self.state='down'
			#	self.moving=True
			if derp and derp2:
				self.xvel=0
				self.moving=False
				#self.yvel=0
				self.set_state_and_frame(self.state,self.frame)
			
			if self.counter>=100 and self.moving:
				self.counter=0
				if self.frame==len(self.animation.states[self.state])-1:
					self.frame=0
					self.set_state_and_frame(self.state,self.frame)
				else:
					self.frame+=1
					self.set_state_and_frame(self.state,self.frame)
			self.bottomed=False
			#print(self.xvel)
			self.rect.x+=self.xvel*(delta/100)
			self.collide(self.xvel,0)
			#self.collided=False
					#print(self.collided)
			#if self.collided==False:
			#	pass
			self.rect.top += self.yvel*(delta/100)
			if not self.is_grounded:
				self.yvel+=50*(delta/100)
				self.collide(0,self.yvel)
				if self.yvel>self.max_gravity:	self.yvel=self.max_gravity
			

					#self.grounded=False
					#if sprite.rect.collidepoint(self.rect.centerx,self.rect.bottom+4):
					#	self.grounded=True
					#if self.grounded==True:
					#	self.yvel=0
					#else:
					#	self.yvel=1
			#for x in self.c_layers[0]:
				#pygame.draw.rect(sender.screen,(222,222,222),(x.rect.x+700,x.rect.y,x.rect.x+(x.rect.width+700),x.rect.y+(x.rect.height)),2)
		#print(self.rect.x,self.rect.y)
			if self.moving==True:
				self.data+='0'
			else:
				self.data+='1'
	def go(self):
		self.going=True
	def get_ent_rect(self):
		return self.rect
	def set_self_rect(self,rect):
		self.rect=rect
	def collide(self,xvel,yvel):
		for sprite in pygame.sprite.spritecollide(self,self.c_layers[0],False):
			if sprite!=self and sprite not in self.projectiles:
				if yvel>0:
					self.rect.bottom=sprite.rect.top
					self.is_grounded=True
					self.yvel=0
				elif xvel>0: # Moving right; Hit the left side of the wall
					self.rect.right = sprite.rect.left
					#self.xvel=0
					#self.collided=True
				elif xvel<0:
					self.rect.left=sprite.rect.right
					#self.xvel=0
					#self.collided=True
				if yvel<0:
					self.rect.top=sprite.rect.bottom
					self.yvel=0

		
