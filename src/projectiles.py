#  projectiles.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import pygame
import imp
import animations
import libkarten
import os
class PlasmaExplosive(pygame.sprite.Sprite):
	def __init__(self,pos,vel,layer,col_layer,req_update_list,anims,sounds):
		super(PlasmaExplosive,self).__init__()
		self.animation=anims[1]
		if vel[0]>0:
			self.direction='right'
		if vel[0]<0:
			self.direction='left'
		if vel[1]>0:
			self.direction='down'
		if vel[1]<0:
			self.direction='up'
		self.vel=vel
		self.frame=0
		self.explosion_sound,self.blast_sound=sounds
		self.image=self.animation.get_frame(self.direction,self.frame)
		self.rect=self.image.get_rect()
		self.rect.center=pos
		self.reqlayer=req_update_list
		self.add(layer)
		self.explode_animation=anims[0]
		self.c_layer=col_layer
		self.layer=layer
		self.c_layer.append(self)
		self.exploded=False
		self.image=self.image.convert_alpha()
		req_update_list.append(self)
		self.c_layers=None
		self.moving=True
		self.blast_sound.play()
	def tile_kill(self):
		try:
			self.c_layer.remove(self)
		except: pass
		self.kill()
		del self
	def update(self,delta,sender):
		if self.moving:
			self.rect.x+=round(delta*(self.vel[0]))
			self.rect.y+=round(delta*(self.vel[1]))
		if self.frame<len(self.animation.states[self.direction])-1:
			self.frame+=1
		else:
			self.frame=0
		self.image=self.animation.get_frame(self.direction,self.frame)
		for wall in sender.c_map.tiles:	
			if self.rect.colliderect(wall.rect) and  self.c_layer in wall.c_layers and wall!=self and wall !=sender.charcont and not self.exploded:
				self.moving=False
				self.kill()
				self.tile_kill()
				Explosion(self.rect.center,self.layer,self.reqlayer,self.explode_animation,self,self.explosion_sound)
				self.exploded=True
		if self.exploded:
			self.kill()
			self.tile_kill()
			return
		
class Explosion(pygame.sprite.Sprite):
	def __init__(self,pos,layer,req_update_list,anim,sender,exp_sound):
		super(Explosion,self).__init__()
		self.animation=anim
		self.frame=0
		self.image=self.animation.get_frame('on',self.frame)
		self.rect=self.image.get_rect()
		self.rect.center=pos
		self.add(layer)
		self.layer=layer
		self.image=self.image.convert_alpha()
		req_update_list.append(self)
		self.state='on'
		exp_sound.play()
	def update(self,delta,sender):	
		if self.frame<len(self.animation.states[self.state])-1:
			self.frame+=0.6
		else:
			self.kill()
			del self
			return
		self.image=self.animation.get_frame(self.state,round(self.frame))
			
