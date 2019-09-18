import socket, asyncio
import random, sys, time
import playground

class EchoClient(asyncio.Protocol):	
	def __init__(self,test_id):
		self.test_id=test_id

	def connection_made(self, transport):
		self.transport = transport
		self.transport.write('<EOL>\n'.encode())

	def data_received(self, data):
		print(data)
		data=data.decode()
		data=data.split('<EOL>\n')
		for line in data:
			if line!='':
				seli=line.split(' ')
				if 'autograde' in seli:
					self.transport.write(('RESULT,'+self.test_id+'<EOL>\n').encode())
					return

if __name__ == "__main__":
	sw=sys.argv[1:]
	loop = asyncio.get_event_loop()
	coro = playground.create_connection(EchoClient(sw[1]),'20194.0.0.19000',19005)
	client = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		loop.close()
	#client.close()
	#loop.run_until_complete(client.close())
	#loop.run_forever()
	
	loop.close()