from EmailInterface import EmailLedgerInterface
from testing.LedgerTest import LedgerTest

class CommandTest(LedgerTest):

    USER_EMAIL = "UMail"

    def setUp(self):
        self.ledger = EmailLedgerInterface(None, None, None, None)
        self.ledger.debug_mode = True

    def addMe(self, eml_ii, usr_ii, success=True, fail_uname=True):
        pre_msg_length = len(self.ledger.message_list)
        self.addLedgerCommand(self.genEmail(eml_ii),
            "ledger add me %s" % self.genUsername(usr_ii))
        self.ledger.performCommands()

        self.assertEquals(len(self.ledger.message_list),
            pre_msg_length + 1)
        latest_message = self.ledger.message_list[-1]
        self.assertEquals(latest_message.recipient, self.genEmail(eml_ii))

        if success:
            self.assertEquals(latest_message.message, "Successfully added user"
                " %s with email %s." % (self.genUsername(usr_ii),
                self.genEmail(eml_ii)))
        elif fail_uname:
            self.assertEquals(latest_message.message, "%s '%s' already"
                " exists for another user." % ("Username" if fail_uname else
                "Email", self.genUsername(usr_ii) if fail_uname else
                self.genEmail(eml_ii)))

    def addLedgerCommand(self, email, command, success=True):
        pre_length = len(self.ledger.command_queue)
        self.ledger.parseLedgerCommand(email, command)
        post_length = len(self.ledger.command_queue)

        if success:
            pre_length += 1

        self.assertEquals(post_length, pre_length)

