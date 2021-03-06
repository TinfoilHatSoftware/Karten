#  epischekarten.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
class Dummy:
	def add_ent_id_ref(x,y):
		return 1
foobar=Dummy()
n = "[epsiche karten]"
print (n+"Welcome to the Epische Karten map editor!")
print (""" 
 _____      _          _          _   __           _                                           
|  ___|    (_)        | |        | | / /          | |                                          
| |__ _ __  _ ___  ___| |__   ___| |/ /  __ _ _ __| |_ ___ _ __                                
|  __| '_ \| / __|/ __| '_ \ / _ \    \ / _` | '__| __/ _ \ '_ \                               
| |__| |_) | \__ \ (__| | | |  __/ |\  \ (_| | |  | ||  __/ | | |                              
\____/ .__/|_|___/\___|_| |_|\___\_| \_/\__,_|_|   \__\___|_| |_|                              
     | |                                                                                       
     |_|""")
import time
print(n+"Module time loaded.")
import platform
print(n+"Module platform loaded.")
import daswesen
print(n+"Module daswesen loaded.")
import pygame
print(n+"Module pygame loaded.")
import PIL.Image,PIL.ImageTk
print(n+"PIL.Image, PIL.ImageTk imported from module PIL.")
import io
print(n+"Module io loaded.")
import libkarten
print(n+"Module libkarten loaded.")
from tkinter import *
print(n+"* imported from module tkinter.")
from tkinter import ttk
print(n+"ttk imported from module tkinter.")
from tkinter import filedialog
print(n+"filedialog imported from module tkinter.")
from tkinter import messagebox
print(n+"messagebox imported from module tkinter.")
import os
print(n+"Module os loaded.")
import sys
print(n+"Module sys loaded.")
print(n+"Defining global variables.")
map_width = 0
map_height = 0
screen_width = 640
screen_height = 480
camera_surface = None
camera_pos = [0,0]
myclock = None
screen = None
fps_limit = 0
running = True
reqs_update=[]
current_tile = None
global tile_buttons
tile_buttons=[]
global button_imgs
button_imgs=[]
global counter
counter=0
global current_tset
current_tset=''
global current_tile
current_tile=None
global current_layer
current_layer=None
global current_layer_str
current_collision_layers=[]
global enable_brushmode
enable_brushmode=False
global brushxtiles
brushxtiles=0
global brushytiles
brushytiles=0
print(n+"Defining layers.")
layer1 = pygame.sprite.Group()
layer2 = pygame.sprite.Group()
layer3 = pygame.sprite.Group()
layer4 = pygame.sprite.Group()
layer5 = pygame.sprite.Group()
layer1_c = []
layer2_c = []
layer3_c = []
layer4_c = []
layer5_c = []
selected_tiles=[]
nontemp_selected_tiles=[]
print(n+"Layer definitions completed.")
print(n+"Defining global functions.")
testtile=None	
def round32(x): return (x+0b10000) & (~0b11111)
def bad_input():
	print(n+"Invalid input! Quitting!")
	quit()
def quitapp():
	print(n+"Quitting on user request.")
	running = False
def load_tileset():
	global counter
	global current_tset
	folderpath = filedialog.askdirectory()
	tset=os.path.basename(folderpath)
	try:
		map_var.load_tileset(tset)
	except IOError as e:
		print(n+"Invalid tileset directory! Error text is as follows:",e)
		return
	list_tsets_box.insert(END,os.path.basename(folderpath))
	current_tset=tset
	print(n+"Set current tileset to "+current_tset+".")
	update_tile_buttons()
def load_wesen_def():
	global counter
	global current_tset
	folderpath=filedialog.askopenfilename()
	folderpath=folderpath.replace(".py","")
	tset=os.path.basename(folderpath)
	try:
		map_var.load_entdef(tset)
	except IOError:
		print(n+"Invalid/nonexistent entity definition!")
		return
	update_tile_buttons()
	list_tsets_box.insert(END,os.path.basename(folderpath))
	if current_tset=="":
		current_tset=os.path.basename(folderpath)
def change_tset(spam_eggs):
	global current_tset
	time.sleep(0.05)
	if len(list_tsets_box.curselection())==0:
		return
	selection = list_tsets_box.curselection()[0]
	current_tset=list_tsets_box.get(selection)
	update_tile_buttons()
def update_tile_buttons():
	global counter
	global current_tset
	global button_imgs
	global tile_buttons
	for button in tile_buttons:
		button.destroy()
	tile_buttons=[]
	button_imgs=[]
	for tile in map_var.get_tiles_from_tileset(current_tset):
		is_wesen_tset=True
		try:
			map_var.tilesets[current_tset].is_wesen_mockup
		except:
			is_wesen_tset=False
		if is_wesen_tset==False:
			pygame_image = tile.animation.states[list(tile.animation.states.keys())[0]][0]
		else:
			pygame_image=map_var.tilesets[current_tset].thumb
		pil_string_image = pygame.image.tostring(pygame_image,"RGBA")
		pil_image = PIL.Image.fromstring("RGBA",(pygame_image.get_rect().width,pygame_image.get_rect().height),pil_string_image)
		button_imgs.append(PIL.ImageTk.PhotoImage(pil_image))
		tile_buttons.append(Button(tilesets_frame.interior,image=button_imgs[counter]))
		tile_buttons[counter].bind("<ButtonRelease-1>",change_tile)
		tile_buttons[counter].meta_number=counter
		tile_buttons[counter].pack()
		counter+=1
	counter=0
def change_tile(event):
	global current_tile
	current_tile=map_var.get_tile_template(current_tset,event.widget.meta_number)
def add_tile():
	global current_tile
	mpos_l=[0,0]
	mpos_l[0],mpos_l[1]=mse
	mpos_l[0]-=camera_pos[0]
	mpos_l[1]-=camera_pos[1]
	c_temp_layers=""
	for index,layer_svar in enumerate(COL_LAYER_ENABLED):
		if str(layer_svar.get())=='1':
			if index+1==1:
				c_temp_layers+="1 "
			if index+1==2:
				c_temp_layers+="2 "
			if index+1==3:
				c_temp_layers+="3 "
			if index+1==4:
				c_temp_layers+="4 "
			if index+1==5:
				c_temp_layers+="5 "
	if c_temp_layers!="":
		c_temp_layers=c_temp_layers[:-1]
	is_wesen_tset=True
	try:
		map_var.tilesets[current_tset].is_wesen_mockup
	except:
		is_wesen_tset=False
	if is_wesen_tset:
		map_var.tiles.append(daswesen.load_wesen(map_var.tilesets[current_tset].name,(int(mpos_l[0]),int(mpos_l[1])),map_var.layers_l,map_var.collisions_l,map_var.reqs_update))
		return
	if enable_brushmode==True:
		global brushxtiles
		global brushytiles
		print(n+"Drawing brush of size "+str(brushxtiles)+" by "+str(brushytiles))
		i=0
		i2=0
		while i<brushytiles:
			i2=0
			while i2<brushxtiles:
				print(n+"In process of drawing brush of size "+str(brushxtiles)+" by "+str(brushytiles))
				mpos_4=(mpos_l[0]+(i2*current_tile.image.get_rect()[2]),mpos_l[1]+(i*current_tile.image.get_rect()[3]))
				map_var.add_tile(current_tile,current_layer,int(current_layer_str.get()[5]),mpos_4,c_temp_layers)
				print(n+"Creating tile at coordinates "+str(mpos_4))
				i2+=1
			i+=1
	if not enable_brushmode==True:
		map_var.add_tile(current_tile,current_layer,int(current_layer_str.get()[5]),mpos_l,c_temp_layers)
		print(n+"Tile of type "+str(current_tile)+" added at position "+str(mpos_l)+" on layer "+str(current_layer)+" on collision layers: "+str(current_collision_layers)+".")
def update_layer():
	global current_layer_str
	global current_layer
	if str(current_layer_str.get())=='layer1':
		current_layer=layer1
	elif str(current_layer_str.get())=='layer2':
		current_layer=layer2
	elif str(current_layer_str.get())=='layer3':
		current_layer=layer3
	elif str(current_layer_str.get())=='layer4':
		current_layer=layer4
	elif str(current_layer_str.get())=='layer5':
		current_layer=layer5
	print(n+"Current layer changed to "+str(current_layer)+".")
def update_collision_layers():
	print(n+"Updating collision layers to:")
	current_collision_layers=[]
	for index,layer_svar in enumerate(COL_LAYER_ENABLED):
		if str(layer_svar.get())=='1':
			if index+1==1:
				current_collision_layers.append(layer1_c)
			if index+1==2:
				current_collision_layers.append(layer2_c)
			if index+1==3:
				current_collision_layers.append(layer3_c)
			if index+1==4:
				current_collision_layers.append(layer4_c)
			if index+1==5:
				current_collision_layers.append(layer5_c)
	print(current_collision_layers)
def remove_tileset_in_editor():
	time.sleep(0.05)
	if len(list_tsets_box.curselection())==0:
		return
	selection = list_tsets_box.curselection()[0]
	selection=list_tsets_box.get(selection)
	for tile_temp in map_var.get_all_tiles():
		try:
			if tile_temp.tileset_name==selection:
				map_var.kill_tile(tile_temp)
		except AttributeError: pass
	map_var.remove_tileset(selection)
	nontemp_selected_tiles=[]
	update_listbox_tilesets()
def update_listbox_tilesets():
	list_tsets_box.delete(0, END)
	for name,tileset in map_var.get_tilesets_dict().items():
		list_tsets_box.insert(END,name)
def save_map():
	f = open(os.path.join("..","media","maps_xml",map_name_svar.get()+".xml"), 'wb')
	f.write(map_var.make_xml())
def update_brush():
	global brushxtiles
	global brushytiles
	if not brushyvar.get()=='' and not brushyvar.get()=='':
		brushytiles=int(brushyvar.get())
		brushxtiles=int(brushxvar.get())
		print(n+"Brush width set to "+str(brushxtiles)+" by "+str(brushytiles))
def enable_disable_brushmode():
	global enable_brushmode
	if enable_brushmode==True:
		enable_brushmode=False
		print(n+"Brush mode disabled")
	elif enable_brushmode==False:
		enable_brushmode=True
		print(n+"Brush mode enabled.")
try:
	screen_width = int(640)
	screen_height = int(480)
except:
	bad_input()
print(n+"Defining classes.")
class cameraScroller(object):
	def __init__(self):
		reqs_update.append(self)
		print(n+"cameraScroller initialized.")
	def update(self,delta,foo):
		keys=pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			camera_pos[0]+=10
		if keys[pygame.K_RIGHT]:
			camera_pos[0]-=10
		if keys[pygame.K_UP]:
			camera_pos[1]+=10
		if keys[pygame.K_DOWN]:
			camera_pos[1]-=10
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)	
	

input(n+"Creating windows, please keep the command prompt in view at all times in case of important messages. Press enter to continue.")
print(n+"Setting up tkinter and pygame SDL environ variables.")
root = Tk()
root.wm_title("Epische Karten Map Editor")
map_name_svar=StringVar()
current_layer=layer1
current_layer_str=StringVar()
brushyvar=StringVar()
brushxvar=StringVar()
isinbrushmode=StringVar()
current_layer_str.set("layer1")
embed = Frame(root, width=screen_width, height=screen_height)
embed.grid(row=0,column=2)
text = ttk.Button(root, text='Load Tileset', command=load_tileset)
text.grid(row=2,column=2)
text2 = ttk.Button(root, text='Load Entity Definition', command=load_wesen_def)
text2.grid(row=5,column=2)
text3 = ttk.Button(root, text='Update Brush', command=update_brush)
text3.grid(row=6,column=2)
delete_tileset = ttk.Button(root, text='Unload Tileset (this will delete all tile instances from selected tileset)', command=remove_tileset_in_editor)
delete_tileset.grid(row=3,column=2)
is_adding_tiles_v=StringVar()
is_adding_tiles=ttk.Checkbutton(root,text="Add tiles",variable=is_adding_tiles_v)
is_adding_tiles.grid(row=1,column=4)
snap_to_grid_v=IntVar()
snap_to_grid=ttk.Checkbutton(root,text="Snap to grid",variable=snap_to_grid_v)
snap_to_grid.grid(row=0,column=4)
Label(text="Tilesets").grid(row=3,column=0)
Label(text="Press delete key to delete tiles.").grid(row=1,column=2)
save_map_button=ttk.Button(root, text='Save Map', command=save_map)
save_map_button.grid(row=4,column=0)
save_map_field=ttk.Entry(root,textvariable=map_name_svar)
save_map_field.grid(row=5,column=1)
Label(text="Map name:").grid(row=5,column=0)
list_tsets_box=Listbox(root)
brushxfield=ttk.Entry(root,textvariable=brushxvar)
brushxfield.grid(row=6,column=1)
Label(text="Brush width in tiles:").grid(row=6,column=0)
brushyfield=ttk.Entry(root,textvariable=brushyvar)
brushyfield.grid(row=7,column=1)
Label(text="Brush height in tiles:").grid(row=7,column=0)
list_tsets_box=Listbox(root)
list_tsets_box.grid(row=1,column=0)
list_tsets_box.bind("<<ListboxSelect>>", change_tset)
b = ttk.Checkbutton(root, text='Enable Brush Mode',variable=isinbrushmode,command=enable_disable_brushmode)
b.grid(row=4,column=2)
tsets_scrollbar = ttk.Scrollbar(root, orient=VERTICAL)
tsets_scrollbar.config(command=list_tsets_box.yview)
tsets_scrollbar.grid(row=1,column=1,sticky='ns')
tilesets_frame = VerticalScrolledFrame(root, width=screen_width, height = 400)
tilesets_frame.grid(row=0,column=0)
tilesets_frame.interior.config(width=128)
MODES = [
        ("Layer 1", "layer1",1),
        ("Layer 2", "layer2",2),
        ("Layer 3", "layer3",3),
        ("Layer 4", "layer4",4),
        ("Layer 5", "layer5",5)
    ]
for text, mode, row in MODES:
	b = ttk.Radiobutton(root, text=text,variable=current_layer_str, value=mode, command = update_layer)
	b.grid(row=row+1,column=3)
COLLISION_LAYERS = [
        ("Collision Layer 1", "layer1",1),
        ("Collision Layer 2", "layer2",2),
        ("Collision Layer 3", "layer3",3),
        ("Collision Layer 4", "layer4",4),
        ("Collision Layer 5", "layer5",5)
    ]
COL_LAYER_ENABLED = [
	StringVar(),
	StringVar(),
	StringVar(),
	StringVar(),
	StringVar()
	]
for text, mode, row in COLLISION_LAYERS:
	b = ttk.Checkbutton(root, text=text,variable=COL_LAYER_ENABLED[row-1], command = update_collision_layers)
	b.grid(row=row+1,column=5)
root.update()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
if platform.system()=="Windows":
	print(n+"Detected Windows platform, using SDL_VIDEODRIVER windib")
	os.environ['SDL_VIDEODRIVER'] = 'windib'
print(n+"Done.")
print(n+"Initializing pygame.time.Clock object.")
myclock = pygame.time.Clock()
print(n+"Initial tick of clock occurs now.")
try:
	fps_limit = 60
except:
	bad_input()
myclock.tick(fps_limit)
responsetext = input(n+"Create map or open existing? [reply C for create or O for open.]>>>")
if responsetext.lower()=="o":
	f_path=input(n+"Map name to open?>>>")
	print(n+"Setting up graphics frame.")
	root.update()
	pygame.display.init()
	root.update()
	screen = pygame.display.set_mode((screen_width,screen_height))
	print(n+"Creating Karte map object.")
	map_var=libkarten.Karte([layer1,layer2,layer3,layer4,layer5],[layer1_c,layer2_c,layer3_c,layer4_c,layer5_c],reqs_update)
	print(n+"Loading map.")
	map_var.fromxml(f_path,foobar)
	print(n+"Done.")
	root.update()
	pygame.display.flip()
	update_listbox_tilesets()
	current_tset=list(map_var.tilesets.keys())[0]
	change_tset("spam")
elif responsetext.lower()=="c":
	print(n+"Creating Karte map object.")
	map_var=libkarten.Karte([layer1,layer2,layer3,layer4,layer5],[layer1_c,layer2_c,layer3_c,layer4_c,layer5_c],reqs_update)
	print(n+"Setting up graphics frame.")
	pygame.display.init()
	screen = pygame.display.set_mode((screen_width,screen_height))
	pygame.display.flip()	
else:
	bad_input()
print(n+"Initializing camera scroller.")
scroller = cameraScroller()
print(n+"Setup completed!")
while running:
	mse = pygame.mouse.get_pos()
	delta = myclock.tick(60)
	try:
		adding_tiles=int(is_adding_tiles_v.get())
	except: adding_tiles=0
	selected_tiles=[]
	if adding_tiles!=1:
		for tiley in map_var.get_all_tiles():
			recty=tiley.rect
			mpos_l=[0,0]
			mpos_l[0],mpos_l[1]=mse
			mpos_l[0]-=camera_pos[0]
			mpos_l[1]-=camera_pos[1]
			mpos2=(mpos_l[0],mpos_l[1])
			if not enable_brushmode:
				if recty.collidepoint(mpos2):
					selected_tiles.append(tiley)
			if enable_brushmode==True:
				if tiley.rect.colliderect((mpos2[0],mpos2[1],brushxtiles*current_tile.image.get_rect()[2],brushytiles*current_tile.image.get_rect()[3])):
					selected_tiles.append(tiley)
				
	if snap_to_grid_v.get()==1 and adding_tiles==1:
		mpos_l=[0,0]
		mpos_l[0],mpos_l[1]=mse
		mpos_l[0]-=camera_pos[0]
		mpos_l[1]-=camera_pos[1]
		mse3=(round32(mpos_l[0]),round32(mpos_l[1]))
		mse = (mse3[0]+camera_pos[0],mse3[1]+camera_pos[1])
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and adding_tiles==1:
			if current_tile != None:
				add_tile()
			else:
				messagebox.showerror("Epische Karten","Please load a tileset before adding tiles.")
		if adding_tiles!=1 and event.type == pygame.MOUSEBUTTONDOWN:
			if selected_tiles!=[] and not enable_brushmode:
				if selected_tiles[0] in nontemp_selected_tiles:
					nontemp_selected_tiles.remove(selected_tiles[0])
				else:
					nontemp_selected_tiles.append(selected_tiles[0])
			if selected_tiles!=[] and enable_brushmode:
				if selected_tiles[0] in nontemp_selected_tiles:
					for tile in selected_tiles:
						try:
							nontemp_selected_tiles.remove(tile)
						except: pass
				else:
					for tile in selected_tiles:
						nontemp_selected_tiles.append(tile)
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_DELETE:
				for ntemptile in nontemp_selected_tiles:
					map_var.kill_tile(ntemptile)
				nontemp_selected_tiles=[]

	for actor in reqs_update:
		actor.update(delta,None)
	screen.fill((0,0,0))
	oldrects={}
	for r in list(layer1):
		oldrects[r]=(r.rect.x,r.rect.y)
		r.rect.x+=camera_pos[0]
		r.rect.y+=camera_pos[1]
	for r in list(layer2):
		oldrects[r]=(r.rect.x,r.rect.y)
		r.rect.x+=camera_pos[0]
		r.rect.y+=camera_pos[1]
	for r in list(layer3):
		oldrects[r]=(r.rect.x,r.rect.y)
		r.rect.x+=camera_pos[0]
		r.rect.y+=camera_pos[1]
	for r in list(layer4):
		oldrects[r]=(r.rect.x,r.rect.y)
		r.rect.x+=camera_pos[0]
		r.rect.y+=camera_pos[1]
	for r in list(layer5):
		oldrects[r]=(r.rect.x,r.rect.y)
		r.rect.x+=camera_pos[0]
		r.rect.y+=camera_pos[1]
	layer1.draw(screen)
	layer2.draw(screen)
	layer3.draw(screen)
	layer4.draw(screen)
	layer5.draw(screen)
	for r in list(layer1):
		r.rect.x,r.rect.y=oldrects[r]
	for r in list(layer2):
		r.rect.x,r.rect.y=oldrects[r]
	for r in list(layer3):
		r.rect.x,r.rect.y=oldrects[r]
	for r in list(layer4):
		r.rect.x,r.rect.y=oldrects[r]
	for r in list(layer5):
		r.rect.x,r.rect.y=oldrects[r]
	if adding_tiles==1:
		nontemp_selected_tiles=[]
	for tilentemp in nontemp_selected_tiles:
		pygame.draw.rect(screen,(0,255,0,30),(tilentemp.rect.x+camera_pos[0],tilentemp.rect.y+camera_pos[1],tilentemp.rect.width,tilentemp.rect.height),2)
	for tiles_s_temp in selected_tiles:
		pygame.draw.rect(screen,(255,0,0,30),(tiles_s_temp.rect.x+camera_pos[0],tiles_s_temp.rect.y+camera_pos[1],tiles_s_temp.rect.width,tiles_s_temp.rect.height),1)
	if adding_tiles==1:
		try:
			is_wesen_mockup=True
			try:
				map_var.tilesets[current_tset].is_wesen_mockup
			except:
				is_wesen_mockup=False
			if is_wesen_mockup==False:
				ctile_rect=current_tile.image.get_rect()
				ctile_rect.x,ctile_rect.y=mse
				screen.blit(current_tile.image,ctile_rect)
			else:
				ctile_rect=map_var.tilesets[current_tset].thumb.get_rect()
				ctile_rect.x,ctile_rect.y=mse
				screen.blit(map_var.tilesets[current_tset].thumb,ctile_rect)
				
		except AttributeError: pass
	try:
		if enable_brushmode==True:
			pygame.draw.rect(screen,(255,0,0,30),(mse[0],mse[1],ctile_rect.w*brushxtiles,ctile_rect.h*brushytiles),2)
	except: pass
	pygame.display.flip()
	try:
		root.update()
	except TclError:
		input(n+"Quit button pressed. Press enter to exit.")
		sys.exit()
	

	
	




