#!python
import netwerk
import threadsutil
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
	myreactor.listenTCP(PORT, netwerk.GameServerFactory('test_map'))
if mode=='client':
	myreactor.connectTCP(HOST,PORT,netwerk.GameClientFactory())
myreactor.run()
while True:
	ans=input('Hullo>')
	if ans=='exitreactor':
		myreactor.stop()
	print(sync_recv)
