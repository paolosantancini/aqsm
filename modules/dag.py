"""
IOTA DAG OBJECT CLASS

@author: Paolo Santancini
"""

from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString

class Dag:

    def __init__(self, api_url, address):
        self.api = api_url
        self.address = address
        
    def doTransaction(self, message):
        api = Iota(self.api, testnet = True)
        msg = TryteString.from_unicode(message)
        tx = ProposedTransaction(address = Address(self.address),message = msg,value = 0)
        result = api.send_transfer(transfers = [tx])
        return(result['bundle'].tail_transaction.hash)
