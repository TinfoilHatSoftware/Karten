#  game.tgsource.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import pygame
global mono_font
mono_font = pygame.font.SysFont("Copperplate Sans", 20)
global energy_label
energy_label=mono_font.render("Energy",False,(128,128,128))
energy_label=energy_label.convert()

def update(delta,c_map,sender):
	global mono_font
	global energy_label
	pygame.draw.rect(sender.screen,(128,128,128),(10,10,201,15),2)
	sender.screen.blit(energy_label,(80,30))
	pygame.draw.rect(sender.screen,(0,255,0),(11,11,sender.charcont.energy,13))
	
