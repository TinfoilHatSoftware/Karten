#  game.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
from os.path import join as jpath
import pygame
import libkarten
import imp
class Game(object):
	def __init__(self):
		self.fp=open(jpath("..","game",'game.tgf'),mode='r')
		self.fp.seek(0)
		for line in self.fp.readlines():
			if line.split()[0]=='resolution':
				xres,yres=line.split('resolution', 1)[1].strip('\n').split()
		self.fp.seek(0)
		self.screen=pygame.display.set_mode((int(xres),int(yres)))
		self.layer1 = pygame.sprite.Group()
		self.layer2 = pygame.sprite.Group()
		self.layer3 = pygame.sprite.Group()
		self.layer4 = pygame.sprite.Group()
		self.layer5 = pygame.sprite.Group()
		self.layer1_c = []
		self.layer2_c = []
		self.layer3_c = []
		self.layer4_c = []
		self.layer5_c = []
		self.reqs_update=[]
	def load(self):
		self.fp.seek(0)
		self.clock=pygame.time.Clock()
		for line in self.fp.readlines():
			if line.split()[0]=='name':
				self.name=line.split('name', 1)[1].strip('\n')
				if self.name[0]==' ':
					self.name=self.name[1:]
				self.n='['+self.name+']'
				print(self.n+'Loading up.')
			if line.split()[0]=='caption':
				pygame.display.set_caption(line.split('caption', 1)[1].strip('\n')[1:])
			if line.split()[0]=='codefile':
				code_path_orig=line.split('codefile', 1)[1].strip('\n')[1:]
				code_path=code_path_orig+'.py'
				self.game_code=imp.load_source(code_path_orig,jpath('..','game',code_path))
			if line.split()[0]=='mapfiles':
				lineremainder=line.split('mapfiles',1)[1]
				self.maparray=lineremainder[1:].strip('\n').split()
			if line.split()[0]=='initial_map':
				lineremainder=line.split('initial_map',1)[1]
				self.initial_map=lineremainder[1:].strip('\n')
		self.fp.seek(0)
		print(self.n+'Done.')
	def run(self):
		print(self.n+'Running.')
		self.c_map=libkarten.Karte([self.layer1,self.layer2,self.layer3,self.layer4,self.layer5],[self.layer1_c,self.layer2_c,self.layer3_c,self.layer4_c,self.layer5_c],self.reqs_update)
		self.c_map.fromxml(self.initial_map)
		for ent in self.reqs_update:
			try:
				ent.go()
			except NameError as e:
				print(self.n+'Warning:Ent '+str(ent)+' does not have method go, ignoring.')
		self.running=True
		self.clock.tick(60)
		while self.running:
			delta=self.clock.tick(60)
			self.screen.fill((0,0,0))
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					self.running = False
					pygame.display.quit()
			self.game_code.update(delta,self.c_map)
			for ent in self.reqs_update:
				ent.update(delta)
			self.layer1.draw(self.screen)
			self.layer2.draw(self.screen)
			self.layer3.draw(self.screen)
			self.layer4.draw(self.screen)
			self.layer5.draw(self.screen)
			pygame.display.flip()
		
		
		
