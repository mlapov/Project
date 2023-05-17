import logging
import queue
import socket

from ibapi import (decoder, reader, comm)
from ibapi.connection import Connection
from ibapi.message import OUT
from ibapi.common import * # @UnusedWildImport
from ibapi.contract import Contract
from ibapi.order import Order, COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID
from ibapi.execution import ExecutionFilter
from ibapi.scanner import ScannerSubscription
from ibapi.comm import (make_field, make_field_handle_empty)
from ibapi.utils import (current_fn_name, BadMessage)
from ibapi.errors import * #@UnusedWildImport
from ibapi.server_versions import * # @UnusedWildImport
from ibapi.utils import ClientException
logger = logging.getLogger(__name__)

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract



import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Msg: ", reqId, " ", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)




    def run(self):
        a = 0
        try:
            while self.isConnected() or not self.msg_queue.empty():
                self.message_handler_terminal()
                a = a + 1
                print('a = ', a)

        finally:
            self.disconnect()

    def message_handler_terminal(self):
        try:
            try:
                text = self.msg_queue.get(block=True, timeout=0.2)
                if len(text) > MAX_MSG_LEN:
                    self.wrapper.error(NO_VALID_ID, BAD_LENGTH.code(),
                                       "%s:%d:%s" % (BAD_LENGTH.msg(), len(text), text))
                    return  # break
            except queue.Empty:
                logger.debug("queue.get: empty")
                self.msgLoopTmo()
            else:
                fields = comm.read_fields(text)
                logger.debug("fields %s", fields)
                self.decoder.interpret(fields)
                self.msgLoopRec()
        except (KeyboardInterrupt, SystemExit):
            logger.info("detected KeyboardInterrupt, SystemExit")
            self.keyboardInterrupt()
            self.keyboardInterruptHard()
        except BadMessage:
            logger.info("BadMessage")

        logger.debug("conn:%d queue.sz:%d",
                     self.isConnected(),
                     self.msg_queue.qsize())




def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 1)  # Should be a pause afterwards before invoking functions

    contract = Contract()
    contract.symbol = "MES"
    contract.secType = "FUT"
    contract.exchange = "GLOBEX"
    contract.currency = "USD"
    contract.localSymbol = "MESU2"
    # contract.primaryExchange = "NASDAQ"

    time.sleep(1)
    app.reqContractDetails(1, contract)

    app.run()




if __name__ == "__main__":
    main()
