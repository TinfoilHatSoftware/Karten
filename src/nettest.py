#!python
import netwerk
import threadsutil
def callback(syncrecv,network):
	return syncrecv.decode('utf8')
mode=input("Mode? S=server, C=client>>>")
if mode.lower()=="s":
	mode='server'
elif mode.lower()=="c":
	mode='client'
else:
	print(n+"Invalid response. Quitting.")
	quit()
if mode=='server':
	manager=netwerk.ThreadedSyncManagerWithMapDownloaderServerSide('25565','test_map')
	manager.listen()
if mode=='client':
	manager=netwerk.ThreadedSyncManagerWithMapDownloaderClientSide('25565','127.0.0.1',callback)
	manager.connect()
manager.run()
while True:
	pass

