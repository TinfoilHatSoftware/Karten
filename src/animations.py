#  animations.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import xml.etree.cElementTree as ET
import pygame
from os import path
class XMLAnimation:
	def __init__(self,folder_name):
		self.states = {}
		print("[animations.py]Initializing XMLAnimation class for "+str(folder_name)+".")
		self.frames_temp = []
		self.path_from_here = path.join("..","media","images","polyimage_sprites",folder_name)
		print("[animations.py]Initializing cElementTree for reading of XML animation data.")
		self.xml_tree = ET.parse(path.join(self.path_from_here,"anim.xml"))
		self.xml_tree_root = self.xml_tree.getroot()
		for state in self.xml_tree_root.findall("state"):
			print("[animations.py]Reading state data from XML:"+str(state)+".")
			self.frames_temp=[]
			for frames in state.findall("frames"):
				print("[animations.py]Reading framelist data from XML:"+str(frames)+" for state "+str(state))
				i=0
				i = int(frames.get("frame_start_num"))
				while i < int(frames.get("frame_start_num"))+int(frames.get("num_frames")):
					self.frames_temp.append(pygame.image.load(path.join(self.path_from_here,"imgs",(frames.get("frame_prefix")+str(i)+self.xml_tree_root.get("fileext")))))
					i+=1
			self.states[state.get("name")] = self.frames_temp
		print("[animations.py]Read state:framelist combos:"+str(self.states)+".")
		self.xml_tree=None
		self.xml_tree_root=None
		keys=list(self.states.keys())
		for key in keys:
			for frame in self.states[key]:
				frame=frame.convert_alpha()
	def get_frame(self,state_name,frame_num):
		return self.states[state_name][frame_num]
class XMLTileAnimation:
	def __init__(self,folder_name,anim_name):
		self.anim_name=anim_name
		self.states = {}
		print("[animations.py]Initializing XMLTileAnimation class for "+str(folder_name)+".")
		self.frames_temp = []
		self.path_to_xml_files = path.join("..","media","images","tiles",folder_name)
		print("[animations.py]Initializing cElementTree for reading of XML animation data.")
		self.xml_tree = ET.parse(path.join(self.path_to_xml_files,"anims",self.anim_name))
		self.xml_tree_root = self.xml_tree.getroot()
		for state in self.xml_tree_root.findall("state"):
			print("[animations.py]Reading state data from XML:"+str(state)+".")
			self.frames_temp=[]
			for frames in state.findall("frames"):
				print("[animations.py]Reading framelist data from XML:"+str(frames)+" for state "+str(state))
				i=0
				i = int(frames.get("frame_start_num"))
				while i < int(frames.get("frame_start_num"))+int(frames.get("num_frames")):
					self.frames_temp.append(pygame.image.load(path.join(self.path_to_xml_files,"images",(frames.get("frame_prefix")+str(i)+self.xml_tree_root.get("fileext")))))
					i+=1
			self.states[state.get("name")] = self.frames_temp
		print("[animations.py]Read state:framelist combos:"+str(self.states)+".")
		self.xml_tree=None
		self.xml_tree_root=None
		keys=list(self.states.keys())
		for key in keys:
			for frame in self.states[key]:
				frame=frame.convert_alpha()
	def get_frame(self,state_name,frame_num):
		return self.states[state_name][frame_num]
