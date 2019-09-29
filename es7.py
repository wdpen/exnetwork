import random, getpass, sys, asyncio, os
import playground
from playground.network.packet.fieldtypes import STRING, BUFFER, UINT8, UINT16, BOOL
from playground.network.common import PlaygroundAddress
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes.attributes import Optional
from playground.common.logging import EnablePresetLogging, PRESET_DEBUG, PRESET_VERBOSE
from es7_mypacket import *
from escape_room_006 import *

EnablePresetLogging(PRESET_DEBUG)

sys.path.append('../BitPoints-Bank-Playground3/src')
from CipherUtil import loadCertFromFile
from BankCore import LedgerLineStorage, LedgerLine
from OnlineBank import BankClientProtocol, OnlineBankConfig

bankconfig = OnlineBankConfig()
bank_addr =     bankconfig.get_parameter("CLIENT", "bank_addr")
bank_port = int(bankconfig.get_parameter("CLIENT", "bank_port"))
bank_stack     =     bankconfig.get_parameter("CLIENT", "stack","default")
bank_username  =     bankconfig.get_parameter("CLIENT", "username")
certPath = os.path.join(bankconfig.path(), "bank.cert")
bank_cert = loadCertFromFile(certPath)

#Server_Port_number=1943+int(random.random()*1000)+int(random.random()*1000)
Server_Port_number=18302

async def example_transfer(bank_client, src, dst, amount, memo, transs):
	await playground.create_connection(
			lambda: bank_client,
			bank_addr,
			bank_port,
			family='default'
		)
	print("Connected. Logging in.")

	try:
		await bank_client.loginToServer()
	except Exception as e:
		print("Login error. {}".format(e))
		return False
	#print('111111')
	try:
		await bank_client.switchAccount(src)
	except Exception as e:
		print("Could not set source account as {} because {}".format(
			src,
			e))
		return False
	#print('222222')
	try:
		result = await bank_client.transfer(dst, amount, memo)
	except Exception as e:
		print("Could not transfer because {}".format(e))
		return False
	print
	print('Transfer Money Completed.')
	#print(result.Receipt, result.ReceiptSignature)
	#print(type(result.Receipt), type(result.ReceiptSignature))	
	# pack1= create_game_pay_packet(result.Receipt, result.ReceiptSignature)
	# transs.write(pack1.__serialize__())
	# print('Sent payment proof packet.')	
	return result

def example_verify(bank_client, receipt_bytes, signature_bytes, dst, amount, memo):
	# playground.create_connection(
	# 		lambda: bank_client,
	# 		bank_addr,
	# 		bank_port,
	# 		family='default'
	# 	)
	# print("Connected. Logging in.")
	# bank_client.loginToServer()
	print('DD1')
	if not bank_client.verify(receipt_bytes, signature_bytes):
		Print("Bad receipt. Not correctly signed by bank")
		return False
	print('DD2')
	ledger_line = LedgerLineStorage.deserialize(receipt_bytes)
	print('DD3')
	if ledger_line.getTransactionAmount(dst) != amount:
		Print("Invalid amount. Expected {} got {}".format(amount, ledger_line.getTransactionAmount(dst)))
		return False
	elif ledger_line.memo(dst) != memo:
		Print("Invalid memo. Expected {} got {}".format(memo, ledger_line.memo()))
		return False
	print('DD4')
	return True

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

class EchoServer(asyncio.Protocol):
	def __init__(self):
		self.game=EscapeRoomGame(output=self.senddata)
		self.gameholder='dhaoshu1'
		self.account='dhaoshu1_account'
		self.amount=10
		self.unique_id=None

	def connection_made(self, transport):
		self.transport = transport
		print('Info From Server: A client has connected to the game.')

	def data_received(self, data):
		dd=PacketType.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			if (recvpack.DEFINITION_IDENTIFIER=='gameinitplayername'):
				print('Server Received username: ',recvpack.username)
				self.unique_id='Beauty Ball '+str((int(random.random()*10000000)/100))+' '+recvpack.username
				pack1=create_game_require_pay_packet(self.unique_id, self.account, self.amount)
				self.transport.write(pack1.__serialize__())
				print('Server Sent require pay packet.')
				continue
			if (recvpack.DEFINITION_IDENTIFIER=='bankreceiptverify'):
				print('Server Received receipt and receipt_signature.')
				#print('Server Received receipt: ', recvpack.receipt, recvpack.receipt_signature)
				#password = getpass.getpass("Enter password for {}: ".format(self.gameholder))
				password='dpo%symp8h!onic'
				bank_client = BankClientProtocol(bank_cert, self.gameholder, password)
				if (example_verify(bank_client, recvpack.receipt, recvpack.receipt_signature, self.account, self.amount, self.unique_id)):
					print('Server verified the payment, sent starting game response.')
					self.game.create_game()
					self.game.start()		
					for a in self.game.agents:
						asyncio.ensure_future(a)
				else:
					pack1=create_game_response('', 'dead')
					self.transport.write(pack1.__serialize__())
					print('Server Sent rejected response message.')
					loop.stop()
				continue
			if (recvpack.DEFINITION_IDENTIFIER=='gamecommunication') and (zenith_nadir==0):
				if self.game.status == "playing":
					if recvpack.commandd!='':
						print('Sever Received game command:  ', recvpack.commandd)
						output = self.game.command(recvpack.commandd)
				if self.game.status!='playing':
					loop.stop()
				continue

	def senddata(self,outdata):
		print('Sent game response message: ', outdata)
		packk=create_game_response(outdata, self.game.status)
		self.transport.write(packk.__serialize__())

	def connection_lost(self,exc):
		self.transport.close()

class EchoClient(asyncio.Protocol):	
	def __init__(self):
		self.escapestep=['look mirror','get hairpin','unlock chest with hairpin',
							'open chest','get hammer in chest','hit flyingkey with hammer',
							'get key','unlock door with key','open door']
		self.es_iter=0;
		self.es_itst=5;
		self.fla=0;
		self.username='dhaoshu1'
		self.useraccount='dhaoshu1_account'

	def connection_made(self, transport):
		self.transport = transport
		pack1=AutogradeStartTest(name='Haoshuai Ding',team=7,email='dhaoshu1@jhu.edu',port=Server_Port_number,packet_file=b'')
		with open('es7_mypacket.py','rb') as f:
			pack1.packet_file=f.read()
		print('Sent AutogradeStartTest packet.')
		self.transport.write(pack1.__serialize__())

	def data_received(self, data):
		#print(data)
		dd=PacketType.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			#print(recvpack.DEFINITION_IDENTIFIER)
			if recvpack.DEFINITION_IDENTIFIER=='20194.exercise6.autogradesubmitresponse':
				print(recvpack.test_id,recvpack.submit_status,recvpack.client_status,recvpack.server_status,recvpack.error)
				if (self.fla==0):
					pack1=create_game_init_packet(self.username)			
					self.transport.write(pack1.__serialize__())
					print('Sent username packet.',pack1)
					self.fla=1
				continue					

			if recvpack.DEFINITION_IDENTIFIER=='20194.requirepaypacket':
				print(recvpack.unique_id, recvpack.account, recvpack.amount)
				#password = getpass.getpass("Enter password for {}: ".format(self.username))
				password='dpo%symp8h!onic'
				bank_client = BankClientProtocol(bank_cert, self.username, password) 
				result=loop.run_until_complete(example_transfer(bank_client, self.useraccount, recvpack.account, recvpack.amount, recvpack.unique_id, self.transport))
				#asyncio.ensure_future(example_transfer(bank_client, self.useraccount, recvpack.account, recvpack.amount, recvpack.unique_id, self.transport))
				if result:
					print('BBBBBBBBBBBBBB.')
					pack1= create_game_pay_packet(result.Receipt, result.ReceiptSignature)
					self.transport.write(pack1.__serialize__())
					print('Sent payment proof packet.')
				else:
					print('EEfffEeeee.')
				continue

			if (recvpack.DEFINITION_IDENTIFIER=='gamecommunication') and (recvpack.zenith_nadir==1):
				print(recvpack.gameresponse, '   ', recvpack.statusgame)
				if (recvpack.gameresponse!='') and (recvpack.statusgame!='dead'):
					if self.es_iter<len(self.escapestep):
						if self.es_iter!=self.es_itst:
							packk=create_game_command(self.escapestep[self.es_iter])
							print('Sent game command: ',self.escapestep[self.es_iter])
							self.transport.write(packk.__serialize__())
							self.es_iter+=1
						else:
							seli=recvpack.gameresponse.split(' ')
							if (seli[-1]=='wall'):
								packk=create_game_command(self.escapestep[self.es_iter])
								print('Sent game command: ',self.escapestep[self.es_iter])
								self.transport.write(packk.__serialize__())					
								self.es_iter+=1
				continue

			print('Warning: None of the packet Type fits.')

if __name__ == "__main__":
	if ('server' in sys.argv[1:]) or ('client' in sys.argv[1:]):
		if ('server' in sys.argv[1:]):
			loop=asyncio.get_event_loop()
			#coro = playground.create_server(EchoServer,'20191.100.100.1',1810)
			coro = playground.create_server(EchoServer,'localhost',Server_Port_number)
			asyncio.ensure_future(coro)
		else:
			print(bank_addr, bank_port, bank_username)
			yngo=input('If the above message is right, press y: ')
			if yngo=='y':
				loop = asyncio.get_event_loop()
				coro = playground.create_connection(EchoClient,'20194.0.0.19000',19007)
				asyncio.ensure_future(coro)
				#client = loop.run_until_complete(coro)
			else:
				raise Exception('Not able to process.')			
		try:
			loop.run_forever()
		except KeyboardInterrupt:
			loop.stop()
			loop.close()
	else:
		print('Need assigning input argument, server or client.')



