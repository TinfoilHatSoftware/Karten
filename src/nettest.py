#!python
import netwerk
import threadsutil
def callback(syncrecv,network):
	print(n+"In callback.")
	print(syncrecv)
	return sync_send
n='[nettest]'
sync_send=b'gubby'
sync_recv=''
myreactor=threadsutil.ThreadedReactor()
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
if mode=='server':
	myreactor.listenTCP(PORT, netwerk.GameServerFactory('test_map',callback))
if mode=='client':
	myreactor.connectTCP(HOST,PORT,netwerk.GameClientFactory(callback))

myreactor.run(callback)
while True:
	sync_send=input('Hullo>')
	if sync_send=='exitreactor':
		myreactor.stop()
	print(sync_recv)
