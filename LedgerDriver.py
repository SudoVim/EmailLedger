import time
import sys
import socket
from EmailInterface import EmailLedgerInterface

interface = EmailLedgerInterface(sys.argv[1], sys.argv[2], sys.argv[3],
                                 sys.argv[4])
interface.readUsers()
interface.readLedger()

try:
    while True:
        try:
            interface.receiveCommands()
        except socket.gaierror:
            pass
        interface.performCommands()
        interface.sendMessages()
        interface.dumpUsers()
        interface.dumpLedger()
        time.sleep(10)
except KeyboardInterrupt:
    interface.performCommands()
    interface.sendMessages()
    interface.dumpUsers()
    interface.dumpLedger()
