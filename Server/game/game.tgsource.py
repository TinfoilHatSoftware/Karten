#  game.tgsource.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import pygame
import os
global framecount
framecount=0
global timecount
timecount=0

def update(delta,c_map,sender):
	
	global framecount
	global timecount
	global firsttime
	framecount+=1
	timecount+=delta/1000
	if sender.charcont.health<=0:
		teleport_sound2.play()
		sender.charcont.set_rect(pygame.rect.Rect(sender.charcont.original_pos[0],sender.charcont.original_pos[1],sender.charcont.rect[2],sender.charcont.rect[3]))
		sender.charcont.health=200
		sender.charcont.energy=200
		framecount=0
		timecount=0
	
