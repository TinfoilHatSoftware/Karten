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
from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout
n='[netwerks]'
PORT=int(input(n+"Port?>>>"))
mode=input(n+"Mode? S=server, C=client>>>")
if mode.lower()=="s":
	mode='server'
elif mode.lower()=="c":
	mode='client'
else:
	print(n+"Invalid response. Quitting.")
	quit()
if mode=='client':
	HOST=input(n+"Host IP?>>>")
def makebytes(string_var):
	return string_var.encode('utf8')
class GameClientProtocol(LineReceiver):
	def __init__(self):
		pass
    def	lineReceived(self, line):
        stdout.write(str(line.decode('utf8')))

class GameClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print ('Connecting...')

    def buildProtocol(self, addr):
        print ('Connected.')
        return GameClientProtocol()

    def clientConnectionLost(self, connector, reason):
        print ('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print ('Connection failed. Reason:', reason)
class GameServerProtocol(LineReceiver):

	def __init__(self, users, addr):
		self.addr=addr
		self.users = users
		self.username = None
		self.state = "LOGIN"

	def connectionMade(self):
		print(n+"Connection made from client at "+str(self.addr))
		self.sendLine(makebytes('CONNECTED'))
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
		self.state = "GET_MAP"
		print(n+"Connection at address "+str(self.addr)+" set username to "+"'"+str(self.username)+"'")
	def handle_GET_MAP(self,line):
		if line.decode('utf8')=="GOT_MAPS":
			self.state="RUNNING"
			print(n+"Connection with name "+str(self.username)+ " finished getting maps and is now in state RUNNING")
			return
		try:
			self.sendLine(makebytes(str(open(pathjoin("..","media","maps_xml",line.decode('utf8')+'.xml')).read())))
			print(n+"Connection with name "+str(self.username)+ "requested and recieved valid mapfile named "+str(line.decode('utf8')))
		except IOError:
			self.sendLine(makebytes('BAD_MAPNAME'))
			print(n+"Connection with name "+str(self.username)+ " requested invalid map "+str(line.decode('utf8')))
	def handle_RUNNING(self,line):
		for name, protocol in self.users.iteritems():
			if protocol != self:
				protocol.sendLine(makebytes(self.username+" ")+line)
	def lineReceived(self, line):
		if self.state == "LOGIN":
			self.handle_LOGIN(line)
		elif self.state=="GET_MAP":
			self.handle_GET_MAP(line)
		else:
			self.handle_RUNNING(line)


class GameServerFactory(Factory):

	def __init__(self):
		self.users={}

	def buildProtocol(self, addr):
		return GameServerProtocol(self.users,addr)

if mode=='server':
	reactor.listenTCP(PORT, GameServerFactory())
if mode=='client':
	reactor.connectTCP(HOST,PORT,GameClientFactory())
reactor.run()
