from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, INT32, UINT8, BUFFER
from playground.network.packet.fieldtypes.attributes import Optional
import playground

class GameInitPacket(PacketType):
    DEFINITION_IDENTIFIER = "initpacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
      ("username", STRING)
    ]

def create_game_init_packet(u):
    return GameInitPacket(username=u)

def process_game_init(pkt):
    if isinstance(pky, GameInitPacket):
        return pkt.username
    else:
        return False
        #raise Exception('Wrong packet type input.')


class GameRequirePayPacket(PacketType):
    DEFINITION_IDENTIFIER = "requirepaypacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
      ("unique_id", STRING),
      ("account", STRING),
      ("amount", UINT8)
    ]

def create_game_require_pay_packet(un,ac,am):
    return GameRequirePayPacket(unique_id=un, account=ac, amount=am)

def process_game_require_pay_packet(pkt):
    print(isinstance(pky, GameRequirePayPacket))
    if isinstance(pky, GameRequirePayPacket):
        return pkt.unique_id, pkt.account, pkt.amount
    else:
        return False
        #raise Exception('Wrong packet type input.')   


class GamePayPacket(PacketType):
    DEFINITION_IDENTIFIER = "paypacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
      ("receipt", BUFFER),
      ("receipt_signature", BUFFER)
    ]

def create_game_pay_packet(re,resi):
    return GamePayPacket(receipt=re, receipt_signature=resi)

def process_game_pay_packet(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='paypacket'):
        return pkt.receipt, pkt.receipt_signature
    else:
        return False
        #raise Exception('Wrong packet type input.')


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "commandpacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
      ("command", STRING)
    ]

class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "responsepacket"
    DEFINITION_VERSION = "1.0"


    FIELDS = [
      ("response", STRING),
      ("status", STRING),
    ]

def create_game_command(c):
    return GameCommandPacket(command=c)

def create_game_response(re,st):
    return GameResponsePacket(response=re, status=st)

def process_game_command(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='commandpacket'):
        return pkt.command
    else:
        return False
        #raise Exception('Wrong packet type input.')

def process_game_response(pkt):
    if (pkt.DEFINITION_IDENTIFIER=='responsepacket'):
        return pkt.response, pkt.status
    else:
        return False
        #raise Exception('Wrong packet type input.')

if __name__=="__main__":
    pass