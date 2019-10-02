import socket, asyncio
import random, sys, time
import playground
from playground.network.packet.fieldtypes import UINT8, STRING, BUFFER, UINT16, BOOL
from playground.network.common import PlaygroundAddress
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes.attributes import Optional

#Automatic check if the exercise has passed or not
#Input arguments:  test_id host port

#WARNING: this is for the Playground version, not for normal TCP/IP version!

class AutogradeResultRequest(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.autograderesult"
    DEFINITION_VERSION = "1.0"
    
    FIELDS = [
        ("test_id", STRING)
    ]
    
class AutogradeResultResponse(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.autograderesultresponse"
    DEFINITION_VERSION = "1.0"
    
    FIELDS = [
        ("test_id", STRING),
        ("passed", BOOL),
    ]

class EchoClient(asyncio.Protocol):	
	def __init__(self,test_id):
		self.test_id=test_id

	def connection_made(self, transport):
		self.transport = transport		
		pack1=AutogradeResultRequest(test_id=self.test_id)
		self.transport.write(pack1.__serialize__())
		print('requested send')

	def data_received(self, data):
		print(data)
		dd=AutogradeResultResponse.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			print(recvpack.test_id,'\n',recvpack.passed)
		loop.stop()
		loop.close()
		
if __name__ == "__main__":
	sw=sys.argv[1:]
	if sw=='':
		print('Need Input arguments:  test_id host port')
	elif sw[0]=='help':
		print('ONLY for Playground. Input arguments:  test_id host port')
	else:
		loop = asyncio.get_event_loop()
		#coro = playground.create_connection(EchoClient(sw[0]),'20194.0.0.19000',19005)
		#'20194.0.0.19000',19005
		coro = playground.create_connection(lambda:EchoClient(sw[0]),sw[1],int(sw[2]))
		client = loop.run_until_complete(coro)

		try:
			loop.run_forever()
		except KeyboardInterrupt:
			loop.close()
	#client.close()
	#loop.run_until_complete(client.close())
	#loop.run_forever()
		
		loop.close()