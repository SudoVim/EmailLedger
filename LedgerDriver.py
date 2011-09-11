import time
import sys
from EmailInterface import EmailLedgerInterface

interface = EmailLedgerInterface(sys.argv[1], sys.argv[2], sys.argv[3],
                                 sys.argv[4])
interface.readUsers()
interface.readLedger()

try:
    while True:
        interface.receiveCommands()
        interface.performCommands()
        time.sleep(10)
except KeyboardInterrupt:
    interface.performCommands()
