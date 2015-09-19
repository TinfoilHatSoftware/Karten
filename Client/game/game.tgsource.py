#  game.tgsource.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import pygame
import os
mono_font = pygame.font.SysFont("Copperplate Sans", 20)
global energy_label
energy_label=mono_font.render("Energy",False,(128,128,128))
energy_label=energy_label.convert()
global health_label
mono_font2 = pygame.font.SysFont("Copperplate Sans", 20)
health_label=mono_font2.render("Health",False,(128,128,128))
health_label=health_label.convert()
teleport_sound2=pygame.mixer.Sound(os.path.join('..','media','sound','teleport_finish.wav'))
global framecount
framecount=0
global timecount
timecount=0

def update(delta,c_map,sender):
	global mono_font
	global energy_label
	global health_label
	global framecount
	global timecount
	global firsttime
	framecount+=1
	timecount+=delta/1000
	sender.screen.blit(energy_label,(80,30))
	#pygame.draw.rect(sender.screen,(0,255,0),(11,11,sender.charcont.energy,13))
	pygame.draw.rect(sender.screen,(128,128,128),(10,10,201,15),2)

	sender.screen.blit(health_label,(int(sender.xres)-140,30))
	#pygame.draw.rect(sender.screen,(0,255,0),(int(sender.xres)-211,11,sender.charcont.health,13))
	pygame.draw.rect(sender.screen,(128,128,128),(int(sender.xres)-211,10,201,15),2)
	#if sender.charcont.health<=0:
	#	teleport_sound2.play()
	#	sender.charcont.set_rect(pygame.rect.Rect(sender.charcont.original_pos[0],sender.charcont.original_pos[1],sender.charcont.rect[2],sender.charcont.rect[3]))
	#	sender.charcont.health=200
	#	sender.charcont.energy=200
	#	framecount=0
	#	timecount=0
	
