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
	def handle_SETNAME(self,line):
		if line.decode('utf8')=='ACK_LOGIN':
			self.state='GET_MAP_NAME'
			self.username=self.nametmp
			self.nametmp=None
			print(n+"Username successfully set to "+str(self.username))
			self.sendLine(b'GO')
			return
		elif line.decode('utf8')=='TAKEN':
			print(n+"Username taken.")
		self.nametmp=input(n+'Username?>>>')
		self.sendLine(makebytes(self.nametmp))
		print(n+'Requested username as specified. Waiting for response from server.')
	def handle_GET_MAP_NAME(self, line):
		self.mapname=line.decode('utf8')
		self.state="GET_MAP"
		self.sendLine(self.mapname.encode('utf8'))
	def handle_GET_MAP(self, line):
		if os.path.isfile(pathjoin("..","media","maps_xml",self.mapname+".xml")):
			print(n+'Server map already downloaded.')
			self.mappath=pathjoin("..","media","maps_xml",self.mapname+".xml")
			self.sendLine(b'GOT_MAPS')
			self.state='RUNNING'
			self.sendLine(b'RUNNING')
		else:
			self.sendLine(makebytes(self.mapname))
			self.state='RECV_MAP'
	def handle_RECV_MAP(self, line):
		fp=open(pathjoin("..","media","maps_xml",self.mapname+".xml"),'w')
		fp.write(line)
		self.mappath=pathjoin("..","media","maps_xml",self.mapname+".xml")
		self.state='RUNNING'
	def handle_RUNNING(self, line):
		self.sync_send=self.callback(line,self)
		self.sendLine(self.sync_send)
	def	lineReceived(self, line):
		print('[netwerks(debugger)]Recv\'d line:'+line.decode('utf8'))
		print('[netwerks(debugger)]Current state is '+str(self.state))
		if line.decode('utf8')=='MORE_MAPS':
			self.state=='GET_MAP_NAME'
			return
		if self.state=='SETNAME':
			self.handle_SETNAME(line)
		elif self.state=='GET_MAP_NAME':
			self.handle_GET_MAP_NAME(line)
		elif self.state=='RECV_MAP':
			self.handle_RECV_MAP(line)
		elif self.state=='RUNNING':
			self.handle_RUNNING(line)
		elif self.state=='GET_MAP':
			self.handle_GET_MAP(line)
		else:
			self.handle_RUNNING(line)
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

	def __init__(self, users, addr,mapname,callback):
		self.addr=addr
		self.users = users
		self.username = None
		self.callback=callback
		self.mapname=mapname
		self.state = "LOGIN"

	def connectionMade(self):
		print(n+"Connection made from client at "+str(self.addr))
		self.sendLine(b'CONNECTED')
	def connectionLost(self, reason):
		if self.username in self.users:
			del self.users[self.username]
			print(n+'Connection lost from '+str(self.addr))
	def handle_LOGIN(self, name):
		if name in self.users:
			self.sendLine(makebytes('TAKEN'))
			return
		self.sendLine(makebytes('ACK_LOGIN'))
		self.username = name.decode('utf8')
		self.users[name] = self
		self.state = "GET_MAP_NAME"
		print(n+"Connection at address "+str(self.addr)+" set username to "+"'"+str(self.username)+"'")
	def handle_GET_MAP(self,line):
		if line.decode('utf8')=="GOT_MAPS":
			self.state="RUNNING"
			print(n+"Connection with name "+str(self.username)+ " finished getting maps and is now in state RUNNING")
		else:
			try:
				self.sendLine(makebytes(str(open(pathjoin("..","media","maps_xml",line.decode('utf8')+'.xml')).read())))
				print(n+"Connection with name "+str(self.username)+ " requested and recieved valid mapfile named "+str(line.decode('utf8')))
			except IOError:
				self.sendLine(makebytes('BAD_MAPNAME'))
				print(n+"Connection with name "+str(self.username)+ " requested invalid map "+str(line.decode('utf8')))
				time.sleep(5)
	def handle_RUNNING(self,line):
		self.sync_send=self.callback(line,self)
		for name, protocol in self.users.items():
			if protocol != self:
				protocol.sendLine(self.sync_send)
	def handle_GET_MAP_NAME(self,line):
		self.sendLine(makebytes(self.mapname))
		self.sendLine(makebytes(self.mapname))
		self.state="GET_MAP"
	def lineReceived(self, line):
		if self.state == "LOGIN":
			self.handle_LOGIN(line)
		elif self.state=="GET_MAP":
			self.handle_GET_MAP(line)
		elif self.state=="GET_MAP_NAME":
			self.handle_GET_MAP_NAME(line)
		else:
			self.handle_RUNNING(line)


class GameServerFactory(Factory):

	def __init__(self,mapname,callback):
		self.users={}
		self.mapname=mapname
		self.callback=callback

	def buildProtocol(self, addr):
		return GameServerProtocol(self.users,addr,self.mapname,self.callback)


