#  threadsutil.py
#  
#  Copyright 2014 Jacob Swart
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import threading
from twisted.internet import reactor
class Daemon(object):
	def __init__(self,func,arguments):
		self.func=func
		self.args=arguments
		self.running=False
		def _thread():
			while self.running==True:
				self.func(*self.args)
				if self.args!=[]:
					self.args=[]
		self.thread=threading.Thread(target=_thread,args=[])
		self.thread.daemon=True
	def start(self,callback):
		self.args=[callback]
		self.running=True
		self.thread.start()
	def stop(self):
		self.running=False
class ThreadedReactor(object):
	def __init__(self):
		self.daemon=Daemon(self._runreactor,[])
		self.stopped=False
	def _runreactor(self,callback):
		while self.stopped==False:
			reactor.run(installSignalHandlers=0)
	def listenTCP(self,port,factory):
		reactor.listenTCP(port,factory)
	def connectTCP(self,host,port,factory):
		reactor.connectTCP(host,port,factory)
	def run(self,callback):
		self.daemon.start(callback)
	def stop(self):
		reactor.callFromThread(reactor.stop)
		self.stopped=True
		
		
		
