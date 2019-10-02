import random, getpass, sys, asyncio, os
import playground
from playground.network.packet.fieldtypes import STRING, BUFFER, UINT8, UINT16, BOOL
from playground.network.common import PlaygroundAddress
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes.attributes import Optional
from playground.common.logging import EnablePresetLogging, PRESET_DEBUG, PRESET_VERBOSE
from prfc_packet import *
from escape_room_006 import *

EnablePresetLogging(PRESET_DEBUG)

sys.path.append('../BitPoints-Bank-Playground3/src')
from CipherUtil import loadCertFromFile
from BankCore import LedgerLineStorage, LedgerLine
from OnlineBank import BankClientProtocol, OnlineBankConfig

bankconfig = OnlineBankConfig()
# bank_addr =     bankconfig.get_parameter("CLIENT", "bank_addr")
# bank_port = int(bankconfig.get_parameter("CLIENT", "bank_port"))
bank_stack     =     bankconfig.get_parameter("CLIENT", "stack","default")
# bank_username  =     bankconfig.get_parameter("CLIENT", "username")

bank_addr='20194.0.0.19000'
bank_port='777'
bank_username='dhaoshu1'

# certPath = os.path.join(bankconfig.path(), "bank.cert")
certPath = os.path.join('20194_online_bank.cert')
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
	try:
		await bank_client.switchAccount(src)
	except Exception as e:
		print("Could not set source account as {} because {}".format(src,e))
		return False
	try:
		result = await bank_client.transfer(dst, amount, memo)
	except Exception as e:
		print("Could not transfer because {}".format(e))
		return False
	print
	print('Transfer Money Completed.')
	#print(result.Receipt, result.ReceiptSignature)
	#print(type(result.Receipt), type(result.ReceiptSignature))	
	pack1= create_game_pay_packet(result.Receipt, result.ReceiptSignature)
	transs.write(pack1.__serialize__())
	print('Sent payment proof packet.')	
	return result

def example_verify(bank_client, receipt_bytes, signature_bytes, dst, amount, memo):
	if not bank_client.verify(receipt_bytes, signature_bytes):
		print("Bad receipt. Not correctly signed by bank")
		return False
	#print('DD2')
	ledger_line = LedgerLineStorage.deserialize(receipt_bytes)
	if ledger_line.getTransactionAmount(dst) != amount:
		print("Invalid amount. Expected {} got {}".format(amount, ledger_line.getTransactionAmount(dst)))
		return False
	elif ledger_line.memo(dst) != memo:
		print("Invalid memo. Expected {} got {}".format(memo, ledger_line.memo()))
		return False
	#print('DD3')
	return True

class AutogradeStartTest(PacketType):
	DEFINITION_IDENTIFIER = "20194.exercise6.autogradesubmit"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("name", STRING),
		("team", UINT8),
		("email", STRING),
		("port", UINT16)]

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
	def __init__(self, gameholderusername, gameholderaccount, amount):
		self.game=EscapeRoomGame(output=self.senddata)
		self.gameholderusername=gameholderusername
		self.gameholderaccount=gameholderaccount
		self.amount=amount
		self.unique_id=None

	def connection_made(self, transport):
		self.transport = transport
		print('Info From Server: A client has connected to the game.')

	def data_received(self, data):
		dd=PacketType.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			#print(recvpack.DEFINITION_IDENTIFIER)
			if process_game_init(recvpack):
				uusername=process_game_init(recvpack)
				print('Server Received username: ', uusername)
				self.unique_id='Beauty Ball '+str((int(random.random()*10000000)/100))+' '+recvpack.username
				pack1=create_game_require_pay_packet(self.unique_id, self.gameholderaccount, self.amount)
				self.transport.write(pack1.__serialize__())
				print('Server Sent require pay packet.')
				continue
			if process_game_pay_packet(recvpack):
				rreceipt, rreceipt_signature=process_game_pay_packet(recvpack)
				print('Server Received receipt and receipt_signature.')
				#print('Server Received receipt: ', recvpack.receipt, recvpack.receipt_signature)
				#password = getpass.getpass("Enter password for {}: ".format(self.gameholderusername))
				password='hhhh'
				bank_client = BankClientProtocol(bank_cert, self.gameholderusername, password)
				# loop.run_until_complete(example_verify(bank_client, recvpack.receipt, recvpack.receipt_signature,
				# 			self.gameholderaccount, self.amount, self.unique_id, self.transport, self.game))
				if (example_verify(bank_client, rreceipt, rreceipt_signature,
							self.gameholderaccount, self.amount, self.unique_id)):
					print('Server verified the payment, sent starting game response.')
					self.game.create_game()
					self.game.start()		
					for a in self.game.agents:
						asyncio.ensure_future(a)
				else:
					pack1=create_game_response('', 'dead')
					self.transport.write(pack1.__serialize__())
					print('Payment verification failed. Server Sent rejected response message.')
					loop.stop()
					loop.close()
				continue
			if process_game_command(recvpack):
				ccomand=process_game_command(recvpack)
				if self.game.status == "playing":
					if ccommandd!='':
						print('Server Received game command:  ', ccommandd)
						output = self.game.command(ccommandd)
				if self.game.status!='playing':
					loop.stop()
					loop.close()
				continue

	def senddata(self,outdata):
		print('Server Sent game response message: ', outdata, '\t  ',self.game.status)
		packk=create_game_response(outdata, self.game.status)
		self.transport.write(packk.__serialize__())

	def connection_lost(self,exc):
		self.transport.close()

class EchoClient(asyncio.Protocol):	
	def __init__(self, username, useraccount):
		self.escapestep=['look mirror','get hairpin','unlock chest with hairpin',
							'open chest','get hammer in chest','hit flyingkey with hammer',
							'get key','unlock door with key','open door']
		self.es_iter=0;
		self.es_itst=5;
		self.fla=0;
		self.username=username
		self.useraccount=useraccount

	def connection_made(self, transport):
		self.transport = transport
		pack1=AutogradeStartTest(name='Haoshuai Ding',team=3,email='dhaoshu1@jhu.edu',port=Server_Port_number)
		# with open('es7_mypacket.py','rb') as f:
		# 	pack1.packet_file=f.read()		
		self.transport.write(pack1.__serialize__())
		print('Sent AutogradeStartTest packet.')
		print(self.username)

	def data_received(self, data):
		print(data)
		dd=PacketType.Deserializer()
		dd.update(data)
		for recvpack in dd.nextPackets():
			print(recvpack.DEFINITION_IDENTIFIER)
			if recvpack.DEFINITION_IDENTIFIER=='20194.exercise6.autogradesubmitresponse':
				print(recvpack.test_id,recvpack.submit_status,recvpack.client_status,recvpack.server_status,recvpack.error)
				if (self.fla==0):
					pack1=create_game_init_packet(self.username)			
					self.transport.write(pack1.__serialize__())
					print('Sent username packet.')
					self.fla=1
				continue					

			if process_game_require_pay_packet(recvpack):
				uunique_id, aaccount, aamount=process_game_require_pay_packet(recvpack)
				print('Received Required Payment meg: ', uunique_id, aaccount, aamount)
				password = getpass.getpass("Enter bank password for user {}: ".format(self.username))
				bank_client = BankClientProtocol(bank_cert, self.username, password) 
				# result=loop.run_until_complete(example_transfer(bank_client, self.useraccount,
				# 	 recvpack.account, recvpack.amount, recvpack.unique_id, self.transport))
				asyncio.ensure_future(example_transfer(bank_client, self.useraccount, aaccount, aamount, uunique_id, self.transport))
				continue

			if process_game_response(recvpack):
				ggameresponse, sstatusgame=process_game_response(recvpack)
				print('Received game response: ', ggameresponse, '\t  ', sstatusgame)
				if (ggameresponse!='') and (sstatusgame!='dead'):
					if self.es_iter<len(self.escapestep):
						if self.es_iter!=self.es_itst:
							packk=create_game_command(self.escapestep[self.es_iter])							
							self.transport.write(packk.__serialize__())
							print('Sent game command: ',self.escapestep[self.es_iter])
							self.es_iter+=1
						else:
							seli=recvpack.gameresponse.split(' ')
							if (seli[-1]=='wall'):
								packk=create_game_command(self.escapestep[self.es_iter])
								self.transport.write(packk.__serialize__())	
								print('Sent game command: ',self.escapestep[self.es_iter])				
								self.es_iter+=1
				continue

			print('Warning: None of the packet Type fits.')

if __name__ == "__main__":
	if ('server' in sys.argv[1:]) or ('client' in sys.argv[1:]):
		if ('server' in sys.argv[1:]):
			loop=asyncio.get_event_loop()
			#coro = playground.create_server(EchoServer,'20191.100.100.1',1810)
			coro = playground.create_server(lambda:EchoServer('dhaoshu1','dhaoshu1_account',5),'localhost',Server_Port_number)
			asyncio.ensure_future(coro)
		else:
			print('The bank client config: ', bank_addr, bank_port, bank_username)
			yngo=input('If the above message is right, continue? [y/n]: ')
			if yngo=='y':
				loop = asyncio.get_event_loop()
				coro = playground.create_connection(lambda:EchoClient('dhaoshu1','dhaoshu1_account'),'20194.0.0.19000',19008)
				asyncio.ensure_future(coro)
				#client = loop.run_until_complete(coro)
			else:
				raise Exception('Not able to process, need reconfig.')			
		try:
			loop.run_forever()
		except KeyboardInterrupt:
			loop.stop()
			loop.close()
	else:
		print('Need assigning input argument, server or client.')



