

#  netwerks.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from os.path import join as pathjoin
import os.path
import time
import imp
import traceback
import threadsutil
import pygame
from twisted.internet.protocol import Protocol, ClientFactory
n='[netwerks]'
def makebytes(string_var):
	return string_var.encode('utf8')
class GameClientProtocol(LineReceiver):
	def __init__(self,callback):
		self.state='SETNAME'
		self.mapname=''
		self.callback=callback
		self.username=''
		self.maptext=''
	def connectionMade(self):
		print(n+'Connection  protocol fully initialized.')
	def	lineReceived(self, line):
		#print(str(line)+"HELLO")
		returned=self.callback(line,self)
		if returned!=None:	self.sendLine(returned)
class GameClientFactory(ClientFactory):
    def __init__(self,callback):
        self.callback=callback
    def startedConnecting(self, connector):
        print (n+'Connecting...')

    def buildProtocol(self, addr):
        print (n+'Connected.')
        return GameClientProtocol(self.callback)

    def clientConnectionLost(self, connector, reason):
        print (n+'Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print (n+'Connection failed. Reason:', reason)
class GameServerProtocol(LineReceiver):
	def __init__(self, users, addr,objectx,callback):
		self.addr=addr
		self.users = users
		self.username = None
		self.callback=callback
		self.objectx=objectx
		self.state = "INIT"
		self.n='[netwerks server]'
	def handle_INIT(self,line):
		print(line)
	def connectionMade(self):
		print(self.n+"Connection made from client at "+str(self.addr))
		self.sendLine(conversionist.convertMap(self.objectx))
	def connectionLost(self, reason):
		if self.username in self.users:
			del self.users[self.username]
			print(n+'Connection lost from '+str(self.addr))
	def lineReceived(self, line):
		if self.state=='INIT':
			self.handle_INIT(line)
	def transmit(self,line):
		self.sendLine(line)


class GameServerFactory(Factory):

	def __init__(self,mapname,callback):
		self.users={}
		self.mapname=mapname
		self.callback=callback

	def buildProtocol(self, addr):
		return GameServerProtocol(self.users,addr,self.mapname,self.callback)
class ThreadedSyncManagerClient(object):
	def __init__(self,port,addr,callback):
		self.reactor=threadsutil.ThreadedReactor()
		self.PORT=int(port)
		self.callback=callback
		self.HOST=addr
	def connect(self):
		self.reactor.connectTCP(self.HOST,self.PORT,GameClientFactory(self.callback))
	def run(self):
		self.reactor.run(self.callback)
	def stop(self):
		#Destroy this class instance after this, not safe to call run() to restart
		self.reactor.stop()
		
class ThreadedSyncManagerServer(object):
	def __init__(self,port,objectx):
		self.reactor=threadsutil.ThreadedReactor()
		self.PORT=int(port)
		self.objectx=objectx
	def listen(self):
		self.reactor.listenTCP(self.PORT, GameServerFactory(self.objectx,self._callback))
	def run(self):
		self.reactor.run(self._callback)
	def stop(self):
		#Destroy this class instance after this, not safe to call run() to restart
		self.reactor.stop()
	def _callback(self,syncrecv,network):
		return syncrecv.decode('utf8')
class NetworkCoordinator(object):
	def __init__(self,port,host,owned):
		self.manager=ThreadedSyncManagerClient(port,host,self._callback)
		self.manager.connect()
		self.manager.run()
		self.id_num=0
		self.own=owned
		self.latest_data={}
		self.rects={}
		self.out_text={}
	def add_ent(self,ent):
		self.rects[ent.ent_id]=[ent.set_rect,list(ent.get_rect()),ent.get_rect]
	def del_ent(self,ent):
		del self.rects[ent.ent_id]
	def _callback(self,line,protocool):
		print(line)
		try:
			for k,v in eval(line.decode().replace('RUNNING','')).items():
				self.latest_data[k]=v
		except (SyntaxError) as e: print(str(traceback.print_exc()))
		return str(self.out_text)
	def update(self):
		print(self.latest_data,self.own)
		for k,v in self.latest_data.items():
			if self.own:
				self.rects[k][0](pygame.rect.Rect(v))
		for key,value in self.rects.items():
			self.rects[key][1]=value[2]()
		self.out_text={}
		for ent_id,rect_methods in self.rects.items():
			self.out_text[ent_id]=(rect_methods[1][0],rect_methods[1][1],rect_methods[1][2],rect_methods[1][3])
	def stop(self):
		self.manager.stop()
		del self.manager
		print(n+'Stopped network daemon.')
		


