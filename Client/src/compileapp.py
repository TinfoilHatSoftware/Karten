# compileapp.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
import sys
from cx_Freeze import setup, Executable
base = None
setup(  name = "game",version = "0.1",description = "Game executable",executables = [Executable("launcher.py", base=base)])
