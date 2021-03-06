#  game.py
#
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
from os.path import join as jpath
import pygame
import timeit
import time
from itertools import zip_longest
import libkarten, random
import imp
import conversionist
import netwerk
class Game(object):
	def __init__(self):
		#self.PYGAME_KEY_CONVERSION_BASE={pygame.K_a:'a',pygame.K_w:'w',pygame.K_d='d'}
		self.PYGAME_KEY_CONVERSION_BASE={}
		self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE
		self.fp=open(jpath("..","game",'game.tgf'),mode='r')
		self.fp.seek(0)
		for line in self.fp.readlines():
			if line.split()[0]=='resolution':
				#self.xres,self.yres=line.split('resolution', 1)[1].strip('\n').split()
				self.xres,self.yres=(1600,900)
		self.fp.seek(0)
		self.screen=pygame.display.set_mode((int(self.xres),int(self.yres)),self.flags)
		self.layer1 = pygame.sprite.Group()
		self.layer2 = pygame.sprite.Group()
		self.layer3 = pygame.sprite.Group()
		self.layer4 = pygame.sprite.Group()
		self.layer5 = pygame.sprite.Group()
		self.alpha_test_map=pygame.image.load('../media/alpha_darkness_1.png').convert_alpha()
		self.layer1_c = []
		self.layer2_c = []
		self.layer3_c = []
		self.protocol=None
		self.ents_by_id={}
		self.shaking=False
		self.shakes=0
		self.shakesize=0
		self.curr_id=0
		self.map_data=None
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
		# Avoid dot lookups; they're slow
		yres = self.yres
		xres = self.xres
		screenref = self.screen
		increasePos = self.increasePos
		decreasePos = self.decreasePos

		self.c_map=libkarten.Karte([self.layer1,self.layer2,self.layer3,self.layer4,self.layer5],[self.layer1_c,self.layer2_c,self.layer3_c,self.layer4_c,self.layer5_c],self.reqs_update)
		self.netmgr=netwerk.ThreadedSyncManagerClient(26642,'127.0.0.1',self._netcallback)
		self.netmgr.connect()
		self.netmgr.run()
		for tile in self.c_map.tiles:
			is_wesen=True
			try:
				tile.is_wesen
			except AttributeError:
				is_wesen=False
			if is_wesen and tile.name=='derp':
				pass
		for ent in self.reqs_update:
			try:
				ent.go()
			except NameError as e:	pass
				#print(self.n+'Warning:Ent '+str(ent)+' does not have method go, ignoring.')
		time.sleep(2)
		self.running=True
		self.clock.tick(500)
		print(self.n+'Running.')
		while self.running:
			delta=self.clock.tick(500)
			mse = pygame.mouse.get_pos()
			sprites1=self.layer1.sprites()
			sprites2=self.layer2.sprites()
			sprites3=self.layer3.sprites()
			sprites4=self.layer4.sprites()
			sprites5=self.layer5.sprites()
			mpos_l=[0,0]
			mpos_l[0],mpos_l[1]=mse
			mpos_l[0] -= self.camera_pos[0]
			mpos_l[1] -= self.camera_pos[1]
			self.mouse_pos=(mpos_l[0],mpos_l[1])
			screenref.fill((0,0,0))
			for e in pygame.event.get(pygame.QUIT):
				if e.type == pygame.QUIT:
					self.running = False
			for ent in self.reqs_update:
				ent.update(delta,self)
			keys=pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				self.running=False
			oldrects={}
			shook=False
			if self.locking==True:
				self.camera_pos=(-self.entrectref().center[0]+(xres/2),-self.entrectref().center[1]+(yres/2))
			if self.shaking and self.shakes>0:
				valy=int(random.uniform(-1.0,1.0)*self.shakesize)
				valx=int(random.uniform(-1.0,1.0)*self.shakesize)
				self.camera_pos=(self.camera_pos[0]+valx,self.camera_pos[1]+valy)
				shook=True
				self.shakes-=1
			if self.shakes==0:
				self.shaking=False
			t1=timeit.default_timer()
			#for r in list(self.layer3):
			#	oldrects[r]=(r.rect.x,r.rect.y)
			#	r.rect.x+=self.camera_pos[0]
			#	r.rect.y+=self.camera_pos[1]
			cposx, cposy = self.camera_pos
			for group in zip_longest(sprites1, sprites2, sprites3, sprites4, sprites5):
				increasePos(*group, cposx=cposx, cposy=cposy)
			t2=timeit.default_timer()

			screfblit = screenref.blit
			for sprite in sprites1:
				if sprite.rect.colliderect((0,0,xres,yres)):
					screfblit(sprite.image,sprite.rect)

			for sprite in sprites2:
				if sprite.rect.colliderect((0,0,xres,yres)):
					screfblit(sprite.image,sprite.rect)

			for sprite in sprites3:
				if sprite.rect.colliderect((0,0,xres,yres)):
					screfblit(sprite.image,sprite.rect)

			for sprite in sprites4:
				if sprite.rect.colliderect((0,0,xres,yres)):
					screfblit(sprite.image,sprite.rect)

			for sprite in sprites5:
				if sprite.rect.colliderect((0,0,xres,yres)):
					screfblit(sprite.image,sprite.rect)

			print(t2-t1)
			#for r in list(self.layer3):
			#	r.rect.x,r.rect.y=oldrects[r]
			for group in zip_longest(sprites1, sprites2, sprites3, sprites4, sprites5):
				increasePos(*group, cposx=cposx, cposy=cposy)
			pygame.draw.rect(screenref,(255,255,255),pygame.rect.Rect(cposx,cposy,320,320),2)
			for tile in self.c_map.tiles:
				if tile.rect.colliderect(pygame.rect.Rect(0,0,320,320)):
					pygame.draw.rect(screenref,(255,0,255),(tile.rect[0]+cposx,tile.rect[1]+cposy,32,32),2)
			if shook:
				self.camera_pos = (cposx - valx, cposy - valy)
			self.game_code.update(delta,self.c_map,self)
			pygame.display.flip()
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
			if self.c_map:
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
	def _netcallback(self,data,sender):
		#print(data)
		if self.protocol!=sender:	self.protocol=sender
		#print("DATA:%s" % str(data))
		try:
			#print(data)
			items=data.decode('utf8')
			#if items[0]!='#':
			#	print(items)
		except:
			#print(data)
			conversionist.reverseConvertMap(data,self.c_map,self)
			return
	#	if items[0]=='<':
		#	x=items[1:].split(' ')
		#	rect=pygame.rect.Rect(int(x[0]),int(x[1]),int(x[2]),int(x[3]))
	#		self.c_map.remove_rect(rect)
	#		self.c_map.remove_rect(rect)
		if items[0]=='#':
			pass
		elif items[0]=='@':
			x=items[1:].split(' ')
			print(x)
			self.c_map.loadWesenWithID(x[0],(int(x[1]),int(x[2])),self.reqs_update,int(x[3]),self,int(x[4]))
			return
		else:
			self.id_num=int(items)
			print(self.n+"Current ID:"+str(self.id_num))
			return
		items=items[1:]
		items=items.split(" ")
		i=1
		y=[]
		z=[]
		#print(items)
		for x in items:
			#print(x)
			if i%3==0 and i!=0:
				y.append(x[2:])
				z.append((y[0],y[1],y[2]))
				y=[]
			else:
				try:
					y.append(int(x))
				except:
					y.append(0)
					print('ISSUE GOIN\' ON HERE')
			i+=1
		items=z
		#print(items)
		##print(self.ents_by_id)
		for idx,ent in self.ents_by_id.items():
			#print(idx)
			ent.rect.x=items[idx][0]
			ent.rect.y=items[idx][1]
			ent.data=items[idx][2]
		keys=pygame.key.get_pressed()
		inputv=''
		if keys[pygame.K_d]:
			inputv+='d '
		if keys[pygame.K_w]:
			inputv+='w '
		if keys[pygame.K_a]:
			inputv+='a '
		try:
			inputv+=' *%s %s ' % (str(round(self.mouse_pos[0])),str(round(self.mouse_pos[1])))
		except BaseException as e:
			#print(e)
			pass
		inputv='$'+inputv
		return inputv.encode('utf8')
	def add_ent_id_ref(self,ent,ent_id=None):
		if ent_id==None:
			self.ents_by_id[self.curr_id]=ent
			ent.id=self.curr_id
		else:
			self.ents_by_id[ent_id]=ent
			ent.id=ent_id
		for key,value in self.ents_by_id.items():
			print(key,value.name)
		self.curr_id+=1
	def cameraShake(self,numshakes,shakesize):
		self.shakes=numshakes
		self.shakesize=shakesize
		self.shaking=True
	def increasePos(self,x1,x2,x3,x4,x5, cposx=0, cposy=0):
		#print(x1,x2,x3,x4,x5)
		if x1:
			x1.rect.x+=cposx
			x1.rect.y+=cposy
		if x2:
			x2.rect.x+=cposx
			x2.rect.y+=cposy
		if x3:
			x3.rect.x+=cposx
			x3.rect.y+=cposy
		if x4:
			x4.rect.x+=cposx
			x4.rect.y+=cposy
		if x5:
			x5.rect.x+=cposx
			x5.rect.y+=cposy
		#print('increasePossing')
	def decreasePos(self,x1,x2,x3,x4,x5, cposx=0, cposy=0):
		if x1:
			x1.rect.x-=cposx
			x1.rect.y-=cposy
		if x2:
			x2.rect.x-=cposx
			x2.rect.y-=cposy
		if x3:
			x3.rect.x-=cposx
			x3.rect.y-=cposy
		if x4:
			x4.rect.x-=cposx
			x4.rect.y-=cposy
		if x5:
			x5.rect.x-=cposx
			x5.rect.y-=cposy
		#print('decreasePossing')
