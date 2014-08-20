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
import netwerk
class Game(object):
	def __init__(self):
		self.flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
		self.fp=open(jpath("..","game",'game.tgf'),mode='r')
		self.fp.seek(0)
		for line in self.fp.readlines():
			if line.split()[0]=='resolution':
				self.xres,self.yres=line.split('resolution', 1)[1].strip('\n').split()
		self.fp.seek(0)
		self.screen=pygame.display.set_mode((int(self.xres),int(self.yres)),self.flags)
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
		self.locking=False
		self.reqs_update=[]
		pygame.mixer.pre_init(44100, 16, 6, 4096)
		pygame.mixer.init()
		print('[launcher]Mixer initialized.')
		pygame.init()
		self.xres=int(self.xres)
		self.yres=int(self.yres)
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
		self.camera_pos=(0,0)
		print(self.n+'Done.')
	def run(self):
		print(self.n+'Running.')
		self.yres=int(self.yres)
		self.xres=int(self.xres)
		owner=input('Owner_id>')
		owned=True
		if owner.lower()=='this':
			owned=True
		elif owner.lower()=='other':
			owned=False
		self.manager=netwerk.NetworkCoordinator('25565','127.0.0.1',owned)
		self.c_map=libkarten.Karte([self.layer1,self.layer2,self.layer3,self.layer4,self.layer5],[self.layer1_c,self.layer2_c,self.layer3_c,self.layer4_c,self.layer5_c],self.reqs_update)
		self.c_map.fromxml(self.initial_map)
		for tile in self.c_map.tiles:
			is_wesen=True
			try:
				tile.is_wesen
			except AttributeError:
				is_wesen=False
			if is_wesen and tile.name=='derp':
				self.manager.add_ent(tile)
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
			for e in pygame.event.get(pygame.QUIT):
				if e.type == pygame.QUIT:
					self.running = False
			for ent in self.reqs_update:
				ent.update(delta,self)
			self.manager.update()
			oldrects={}
			if self.locking==True:
				self.camera_pos=(-self.entrectref().center[0]+self.xres/2,-self.entrectref().center[1]+self.yres/2)
			for r in list(self.layer1):
				oldrects[r]=(r.rect.x,r.rect.y)
				r.rect.x+=self.camera_pos[0]
				r.rect.y+=self.camera_pos[1]
			for r in list(self.layer2):
				oldrects[r]=(r.rect.x,r.rect.y)
				r.rect.x+=self.camera_pos[0]
				r.rect.y+=self.camera_pos[1]
			for r in list(self.layer3):
				oldrects[r]=(r.rect.x,r.rect.y)
				r.rect.x+=self.camera_pos[0]
				r.rect.y+=self.camera_pos[1]
			for r in list(self.layer4):
				oldrects[r]=(r.rect.x,r.rect.y)
				r.rect.x+=self.camera_pos[0]
				r.rect.y+=self.camera_pos[1]
			for r in list(self.layer5):
				oldrects[r]=(r.rect.x,r.rect.y)
				r.rect.x+=self.camera_pos[0]
				r.rect.y+=self.camera_pos[1]
			self.layer1.draw(self.screen)
			self.layer2.draw(self.screen)
			self.layer3.draw(self.screen)
			self.layer4.draw(self.screen)
			self.layer5.draw(self.screen)
			for r in list(self.layer1):
				r.rect.x,r.rect.y=oldrects[r]
			for r in list(self.layer2):
				r.rect.x,r.rect.y=oldrects[r]
			for r in list(self.layer3):
				r.rect.x,r.rect.y=oldrects[r]
			for r in list(self.layer4):
				r.rect.x,r.rect.y=oldrects[r]
			for r in list(self.layer5):
				r.rect.x,r.rect.y=oldrects[r]
			self.game_code.update(delta,self.c_map,self)
			pygame.display.update((0,0,self.xres,self.yres))
		print(self.n+"Runloop stopped.")
	def change_map(self,map_name):
		print(self.n+"Changing map to "+map_name+".")
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
		try:
			if self.c_map!=None:
				self.c_map.uninitialize(self.c_map)
				self.c_map=None
		except NameError as e:
			pass
		self.initial_map=map_name
	def stop(self):
		self.running=False
		self.manager.stop()
		del self.manager
	def lock_camera_to_ent(self,entrectref,entrectref2):
		self.entrectref=entrectref
		self.entrectref2=entrectref2
		self.locking=True
		self.camera_pos=(entrectref()[0],entrectref()[1])
		
		
		
		
		
		
