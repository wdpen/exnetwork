import socket, asyncio
import random, sys, time
import playground
from playground.network.packet.fieldtypes import UINT8, STRING, BUFFER, UINT16, BOOL
from playground.network.common import PlaygroundAddress
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes.attributes import Optional
#import es6_mypacket

class AutogradeStartTest(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.autogradesubmit"
    DEFINITION_VERSION = "1.0"
    
    FIELDS = [
        ("name", STRING),
        ("team", UINT8),
        ("email", STRING),
        ("port", UINT16),
        ("packet_file", BUFFER)]
        
class AutogradeTestStatus(PacketType):
    DEFINITION_IDENTIFIER = "20194.exercise6.autogradesubmitresponse"
    DEFINITION_VERSION = "1.0"
    
    NOT_STARTED = 0
    PASSED      = 1
    FAILED      = 2
    
    FIELDS = [
        ("test_id", STRING),
        ("submit_status", UINT8),
        ("client_status", UINT8),
        ("server_status", UINT8),
        ("error", STRING({Optional: True}))]
        
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
	def __init__(self):
		self.escapestep=['look mirror<EOL>\n','get hairpin<EOL>\n','unlock chest with hairpin<EOL>\n',
							'open chest<EOL>\n','get hammer in chest<EOL>\n','hit flyingkey with hammer<EOL>\n',
							'get key<EOL>\n','unlock door with key<EOL>\n','open door<EOL>\n']
		self.es_iter=0;
		self.es_itst=5;
		self.fla=0;

	def connection_made(self, transport):
		self.transport = transport
		pack1=AutogradeStartTest(name='Haoshuai Ding',team=7,email='dhaoshu1@jhu.edu',port=1810,packet_file=b'')
		'''pack1=AutogradeStartTest()
		pack1.name='Haoshuai Ding'
		pack1.team=7
		pack1.email='dhaoshu1@jhu.edu'
		pack1.port=1080
		pack1.packet_file=b''
		'''
		#with open('es6_mypacket.py','rb') as f:
		#	pack1.packet_file=f.read()
		print(pack1)
		self.transport.write(pack1.__serialize__())

	def data_received(self, data):
		print('reve sth')
		dd=AutogradeTestStatus.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			print(recvpack.DEFINITION_IDENTIFIER)
			print(recvpack.test_id,recvpack.submit_status,recvpack.client_status,recvpack.server_status,recvpack.error)



if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	coro = playground.create_connection(EchoClient,'20194.0.0.19000',19006)
	client = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		loop.close()
	#client.close()
	#loop.run_until_complete(client.close())
	#loop.run_forever()
	
	loop.close()