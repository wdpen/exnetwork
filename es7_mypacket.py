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
    return InitGamePlayernamePacket(username=u)

def process_game_init(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='gameinitplayername'):
        return pkt.username
    else:
        return False
        #raise Exception('Wrong packet type input.')


class PaymentInformationPacket(PacketType):
    DEFINITION_IDENTIFIER = '20194.requirepaypacket'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ("unique_id", STRING),
        ('account', STRING),
        ('amount', INT32)
    ]

def create_game_require_pay_packet(un,ac,am):
    return PaymentInformationPacket(unique_id=un, account=ac, amount=am)

def process_game_require_pay_packet(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='20194.requirepaypacket'):
        return pkt.unique_id, pkt.account, pkt.amount
    else:
        return False
        #raise Exception('Wrong packet type input.')   


class ProvingPaymentPacket(PacketType):
    DEFINITION_IDENTIFIER = 'bankreceiptverify'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ("receipt", BUFFER),
        ('receipt_signature', BUFFER),
    ]

def create_game_pay_packet(re,resi):
    return ProvingPaymentPacket(receipt=re, receipt_signature=resi)

def process_game_pay_packet(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='bankreceiptverify'):
        return pkt.receipt, pkt.receipt_signature
    else:
        return False
        #raise Exception('Wrong packet type input.')


class GameCommunicationPacket(PacketType):
    DEFINITION_IDENTIFIER = 'gamecommunication'
    DEFINITION_VERSION = '1.0'
    #zenith_nadir=0---command;zenith_nadir=1---response;
    FIELDS = [
        ('zenith_nadir', INT32),
        ("commandd", STRING({Optional: True})),
        ('gameresponse', STRING({Optional: True})),
        ('statusgame', STRING({Optional: True}))
    ]

def create_game_command(c):
    return GameCommunicationPacket(zenith_nadir=0, commandd=c)

def create_game_response(re,st):
    return GameCommunicationPacket(zenith_nadir=1, gameresponse=re, statusgame=st)

def process_game_command(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='gamecommunication') and (pkt.zenith_nadir==0):
        return pkt.commandd
    else:
        return False
        #raise Exception('Wrong packet type input.')

def process_game_response(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='gamecommunication') and (pkt.zenith_nadir==1):
        return pkt.gameresponse, pkt.statusgame
    else:
        return False
        #raise Exception('Wrong packet type input.')

if __name__=="__main__":
    pass