#  game.tgsource.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
global counter
counter=0
global changed1
changed1=False
global changed2
changed2=False
def update(delta,c_map,sender):
	global counter
	global changed1
	global changed2
	counter+=delta
	print(counter)
	if counter>=1000*10 and not changed1:
		changed1=True
		sender.stop()
		sender.change_map('test2')
		sender.run()
	if counter>=1000*30 and not changed2:
		changed2=True
		sender.stop()
		sender.change_map('test_map')
		sender.run()
	
	
	
