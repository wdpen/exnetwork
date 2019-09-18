import socket, asyncio
import random, sys, time
import playground

class EchoClient(asyncio.Protocol):	
	def __init__(self):
		pass

	def connection_made(self, transport):
		print('sdfs')
		self.transport = transport
		self.transport.write('<EOL>\n')

	def data_received(self, data):
		print(data)
		self.transport.write('sending')


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	coro = playground.create_connection(EchoClient,'20194.0.0.19000',19005)
	client = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		loop.close()
	#client.close()
	#loop.run_until_complete(client.close())
	#loop.run_forever()
	
	loop.close()