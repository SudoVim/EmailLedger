from EmailInterface import EmailLedgerInterface
from testing.LedgerTest import LedgerTest

class CommandTest(LedgerTest):

    def setUp(self):
        self.ledger = EmailLedgerInterface(None, None, None, None)
        self.ledger.debug_mode = True

    def tearDown(self):
        self.ledger = None

    def addMe(self, uname_idx, email_idx)
