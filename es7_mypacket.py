from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, INT32, BUFFER
from playground.network.packet.fieldtypes.attributes import Optional
import playground

class InitGamePlayernamePacket(PacketType):
    DEFINITION_IDENTIFIER = 'gameinitplayername'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ("username", STRING)
    ]

def create_game_init_packet(u):
    return InitGamePlayernamePacket(usename=u)

def process_game_init(pkt):
    de=PacketType.Deserializer()
    de.update(pkt)
    for recvpack in de.nextPackets():
        if (recvpack.DEFINITION_IDENTIFIER=='gameinitplayername'):
            return recvpack.usename
        else:
            raise Exception('Wrong packet type input.')

class PaymentInformationPacket(PacketType):
    DEFINITION_IDENTIFIER = 'requirepaypacket'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ("unique_id", STRING),
        ('account', STRING),
        ('amount', INT32)
    ]

def create_game_require_pay_packet(un,ac,am):
    return PaymentInformationPacket(unique_id=un, account=ac, amount=am)

def process_game_require_pay_packet(pkt):
    de=PacketType.Deserializer()
    de.update(pkt)
    for recvpack in de.nextPackets():
        if (recvpack.DEFINITION_IDENTIFIER=='requirepaypacket'):
            return recvpack.unique_id, recvpack.account, recvpack.amount
        else:
            raise Exception('Wrong packet type input.')   

class ProvingPaymentPacket(PacketType):
    DEFINITION_IDENTIFIER = 'bankreceiptverify'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ("receipt", STRING),
        ('receipt_signature', STRING),
    ]

def create_game_pay_packet(re,resi):
    return ProvingPaymentPacket(receipt=re, receipt_signature=resi)

def process_game_pay_packet(pkt):
    de=PacketType.Deserializer()
    de.update(pkt)
    for recvpack in de.nextPackets():
        if (recvpack.DEFINITION_IDENTIFIER=='bankreceiptverify'):
            return recvpack.receipt, recvpack.receipt_signature
        else:
            raise Exception('Wrong packet type input.')



class GameCommunicationPacket(PacketType):
    DEFINITION_IDENTIFIER = 'gamecommunication'# whatever you want
    DEFINITION_VERSION = '1.0'# whatever you want
    #zenith_nadir=0---command;zenith_nadir=1---response;
    FIELDS = [
        ('zenith_nadir', INT32)
        ("commandd", STRING({Optional: True})),
        ('gameresponse',STRING({Optional: True})),
        ('statusgame',STRING({Optional: True}))
    ]

def create_game_command(c):
    return GameCommunicationPacket(zenith_nadir=0, commandd=c)

def create_game_response(re,st):
    return GameCommunicationPacket(zenith_nadir=1, gameresponse=re, statusgame=st)

def process_game_command(pkt):
    de=PacketType.Deserializer()
    de.update(pkt)
    for recvpack in de.nextPackets():
        if (recvpack.DEFINITION_IDENTIFIER=='gamecommunication') and (recvpack.zenith_nadir==0):
            return recvpack.commandd
        else:
            raise Exception('Wrong packet type input.')

def process_game_response(pkt):
    de=PacketType.Deserializer()
    de.update(pkt)
    for recvpack in de.nextPackets():
        if (recvpack.DEFINITION_IDENTIFIER=='gamecommunication') and (recvpack.zenith_nadir==1):
            return recvpack.gameresponse, recvpack.statusgame
        else:
            raise Exception('Wrong packet type input.')

if __name__=="__main__":
    lm=GameCommandPacket.create_game_command_packet('sa')
    #lm.commandd='fg'
    ls=GameResponsePacket.create_game_response_packet('b','ve')
    #ls=GameCommandPacket()statusgame
    #ls.commandd='fgerwr'
   # print(GameResponsePacket.response(lm))
    h=ls.status
    print(lm.commandd, ls.game_over(),h())
    pp=b'\x00\x00\x00\x00\x00\x00\x00.\xff\xff\xff\xff\xff\xff\xff\xd1\x0fes6.gamecommand\x031.0\x00\x01\x00\x00\x00\x04look'
    dd1=GameCommandPacket.Deserializer()
    dd1.update(pp)
    for recvpack in dd1.nextPackets():
        if recvpack.commandd=='':
            print('DDDD')
        print(recvpack.commandd)


