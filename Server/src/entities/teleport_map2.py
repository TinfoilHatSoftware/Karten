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
#DIRECTIVE ANIMATION teleporter
#DIRECTIVE POSITION ;
#DIRECTIVE LAYER 3
#DIRECTIVE REQS_UPDATE ;
#END DIRECTIVES
import daswesen
import pygame
import animations
import projectiles
from os.path import join as join
def round32(x): return (x+0b10000) & (~0b11111)
class WesenEnt(daswesen.GrafikWesenBase):
	def __init__(self,animation,position,layer):
		self.layer=layer[1]
		self.name="teleport_map2"
		self.localplayerchar=True
		self.counter=0
		self.xvel=0
		self.yvel=0
		self.frame=0
		self.going=False
		self.moving=False
		self.c_layers=[]
		self.is_wesen=True
		self.firsttime=True
		self.opening=False
		self.framecounter=0
		super(WesenEnt,self).__init__(animation,position,[],[],layer[1],layer[0],('right',0))
	def update(self,delta,sender):
		if self.going==True:
			if self.firsttime==True:
				self.firsttime=False
				self.teleport_sound=pygame.mixer.Sound(join('..','media','sound','teleport.wav'))
				self.teleport_sound2=pygame.mixer.Sound(join('..','media','sound','teleport_finish.wav'))
			#if self.opening:
				#sender.charcont.rect.center=self.charpos
			if self.framecounter<700:
				self.framecounter+=delta
			else:
				self.framecounter=0
				if self.opening:
					if self.frame<len(self.animation.states['right'])-1:
						self.frame+=1
					else:
						self.frame=0
						self.opening=False
						#self.teleport_sound2.play()
						#sender.stop()
						#sender.change_map('test2')
						#sender.run()
			self.state='right'
			self.set_state_and_frame(self.state,self.frame)
			for wall in sender.c_map.tiles:	
				name='derp'
				try:
					wall.name
				except:
					name=None
				if self.rect.colliderect(wall.rect) and wall!=self and not self.opening and name!='derp':
					self.opening=True
					#self.charpos=sender.charcont.rect.center
					self.teleport_sound.play()
			
	def go(self):
		self.going=True
	def tile_kill(self):
		try:
			self.c_layer.remove(self)
		except: pass
		self.kill()
		del self
