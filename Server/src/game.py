#  game.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
from os.path import join as jpath
from pygame.locals import *
import pygame
import sys, select, math, imp
import libkarten, libmapgen, conversionist, netwerk
class Game(object):
	def __init__(self):
		self.fp=open(jpath("..","game",'game.tgf'),mode='r')
		self.fp.seek(0)
		screen = pygame.display.set_mode((800, 600))
		self.layer1 = pygame.sprite.Group()
		self.layer2 = pygame.sprite.Group()
		self.layer3 = pygame.sprite.Group()
		self.layer4 = pygame.sprite.Group()
		self.layer5 = pygame.sprite.Group()
		self.layer1_c = []
		self.layer2_c = []
		self.rem_index_curr=0
		self.layer3_c = []
		self.clients=[]
		self.map_data=None
		self.input={}
		self.ents_by_id={}
		self.curr_id=0
		self.layer4_c = []
		self.layer5_c = []
		self.locking=False
		self.reqs_update=[]
		pygame.init()
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
		self.manager=netwerk.ThreadedSyncManagerServer(26642,self,self._net_callback)
		self.manager.listen()
		self.manager.run()
		self.c_map=libkarten.Karte([self.layer1,self.layer2,self.layer3,self.layer4,self.layer5],[self.layer1_c,self.layer2_c,self.layer3_c,self.layer4_c,self.layer5_c],self.reqs_update)
		#self.c_map.fromxml(self.initial_map,self)
		mapmgr=libmapgen.MapGenerator({'base':0},'derek_terrain',self.c_map)
		mapmgr.add_to_map()
		#print(self.c_map.make_xml())
		for tile in self.c_map.tiles:
			is_wesen=True
			try:
				tile.is_wesen
			except AttributeError:
				is_wesen=False
		for ent in self.reqs_update:
			try:
				ent.go()
			except NameError as e:
				print(self.n+'Warning:Ent '+str(ent)+' does not have method go, ignoring.')
		self.running=True
		self.clock.tick(500)
		while self.running:
			#print(self.c_map.collisions_l)
			delta=self.clock.tick(500)
			#print(round(self.clock.get_fps()))
			pygame.event.pump()
			keys = pygame.key.get_pressed()
			if keys[K_ESCAPE]:
				print(round(self.clock.get_fps()))
			for e in pygame.event.get(pygame.QUIT):
				if e.type == pygame.QUIT:
					self.running = False
			for ent in self.reqs_update:
				ent.update(delta,self)
			self.game_code.update(delta,self.c_map,self)
			bleh=[0] * len(self.ents_by_id.keys())
			for key,value in self.ents_by_id.items():
				bleh[key]=str(value.rect.x)+" "+str(value.rect.y)+" "+str(value.data)
				#print(value.data)
				value.data='000'
			data=' '.join(str(e) for e in bleh)
			data=('#'+data).encode('utf8')
			for x in self.clients:
				x.transmit(data)
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
	def lock_camera_to_ent(self,entrectref,entrectref2):
		self.entrectref=entrectref
		self.entrectref2=entrectref2
		self.locking=True
		self.camera_pos=(entrectref()[0],entrectref()[1])
	def add_ent_id_ref(self,ent):
		self.ents_by_id[self.curr_id]=ent
		ent.id=self.curr_id
		print(self.ents_by_id)
		for key,value in self.ents_by_id.items():
			print(key,value.name)
		self.curr_id+=1
	def _net_callback(self,x,y=None):
		try:
			x=x.decode('utf8')
		except:
			pass
		#print(x,y)
		input=[]
		if not y in self.clients and y!=None:
			self.clients.append(y)
		if x==0:
			idx=self.rem_index_curr
			self.rem_index_curr+=1
			y.idx=idx
			id2=self.curr_id
			ent=self.c_map.loadWesenWithID('derp',(20,-190),self.reqs_update,idx,self)
			for x in range(int(math.ceil(self.c_map.maxx/100))):
				for m in range(int(math.ceil(self.c_map.maxy/100))):
					u=x-1
					v=m-1
					if u<0:
						u=0
					if v<0:
						v=0
					y.sendLine(conversionist.convertMap(self.c_map,pygame.rect.Rect(u*100,v*100,x*100,m*100)))
			y.sendLine(str(idx).encode('utf8'))
			data=('@derp 192 64 %s %s' % (idx,id2)).encode('utf8')
			for each in self.clients:
				each.sendLine(data)
			return
		if x[0]=='$':
			x=x[1:]
			self.input[y.idx]=x
			#print(self.input)

		
		
		
		
		
		
