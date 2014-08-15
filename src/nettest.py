#!python
import netwerk
import threadsutil
import pygame
import time
class Gunk(object):
	def __init__(self):
		self.ent_id=0
		self.rect=pygame.rect.Rect((50,60,10,10))
	def set_rect(self,rect):
		print('setting rect to ',rect)
		self.rect=rect
	def get_rect(self):
		return self.rect
def callback(syncrecv,network):
	return syncrecv.decode('utf8')
mode=input("Mode? S=server, C=client>>>")
owner=input('Owner_id>')
if owner.lower()=='this':
	owned=True
if owner.lower()=='other':
	owned=False
if mode.lower()=="s":
	mode='server'
elif mode.lower()=="c":
	mode='client'
else:
	print(n+"Invalid response. Quitting.")
	quit()
if mode=='server':
	manager=netwerk.ThreadedSyncManagerServer('25565','test_map')
	manager.listen()
	manager.run()
if mode=='client':
	manager=netwerk.NetworkCoordinator('25565','127.0.0.1',owned)
	gunky=Gunk()
	manager.add_ent(gunky)
	time.sleep(1)

while True:
	val=input('Guh>')
	if val=='up':
		gunky.rect.y-=1
	if val=='down':
		gunky.rect.y+=1
	if val=='print':
		print(gunky.rect,manager.rects)
