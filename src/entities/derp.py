#  Entity Defintion
#  
#  Copyright 2014 Jacob Swart
#
#  This entdef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
#
#
#BEGIN DIRECTIVES
#DIRECTIVE ANIMATION mech_tan_resized
#DIRECTIVE POSITION ;
#DIRECTIVE LAYER 3
#DIRECTIVE COLLISION_LAYERS 3
#DIRECTIVE REQS_UPDATE ;
#END DIRECTIVES
import daswesen
class WesenEnt(daswesen.GrafikWesenBase):
	def __init__(self,animation,position,layer,collision_layers):
		self.layer=layer[1]
		self.name="derp"
		self.going=False
		self.is_wesen=True
		super(WesenEnt,self).__init__(animation,position,collision_layers[1],collision_layers[0],layer[1],layer[0],('right',0))
	def update(self,delta):
		if self.going==True:
			self.rect.x+=1
	def go(self):
		self.going=True
		
