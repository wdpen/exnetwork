import asyncio

class EchoClient(asyncio.Protocol):
	def __init__(self):
		pass

	def connection_made(self, transport):
		self.transport = transport
		#self.transport.write("Hello World".encode())

	def data_received(self, data):
		print(data)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	coro = loop.create_connection(EchoClient,'192.168.200.52',19003)
	client = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	#client.close()
	#loop.run_until_complete(client.close())
	#loop.run_forever()
	
	loop.close()
