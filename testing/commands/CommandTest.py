from EmailInterface import EmailLedgerInterface
from testing.LedgerTest import LedgerTest

class CommandTest(LedgerTest):

    BAD_EML = 1
    BAD_UNAME = 2
    BAD_TARGET = 3

    def setUp(self):
        self.ledger = EmailLedgerInterface(None, None, None, None)
        self.ledger.debug_mode = True

    def addMe(self, eml_ii, usr_ii, fail=None):
        fail_uname = fail == self.BAD_UNAME

        pre_msg_length = len(self.ledger.message_list)
        self.addLedgerCommand(self.genEmail(eml_ii),
            "ledger add me %s" % self.genUsername(usr_ii))
        self.ledger.performCommands()
        post_msg_length = len(self.ledger.message_list)

        self.assertEquals(pre_msg_length + 1, post_msg_length)
        latest_message = self.ledger.message_list[-1]
        self.assertEquals(latest_message.recipient, self.genEmail(eml_ii))

        if not fail:
            self.assertEquals(latest_message.message, "Successfully added user"
                " %s with email %s." % (self.genUsername(usr_ii),
                self.genEmail(eml_ii)))
        elif fail_uname:
            self.assertEquals(latest_message.message, "%s '%s' already"
                " exists for another user." % ("Username" if fail_uname else
                "Email", self.genUsername(usr_ii) if fail_uname else
                self.genEmail(eml_ii)))

    def owesMe(self, eml_ii, usr_ii, owes_me=True, fail=None):
        pre_msg_length = len(self.ledger.message_list)

        send_msg = ""
        if owes_me:
            send_msg = "ledger %s owes me $5.00" % self.genUsername(usr_ii)
        else:
            send_msg = "ledger i paid %s $5.00" % self.genUsername(usr_ii)

        self.addLedgerCommand(self.genEmail(eml_ii), send_msg)
        self.ledger.performCommands()
        post_msg_length = len(self.ledger.message_list)

        num_messages = 0
        if not fail:
            num_messages = 2
        else:
            num_messages = 1

        pre_msg_length += num_messages
        latest_messages = self.ledger.message_list[(-1 * num_messages):]

        self.assertEquals(pre_msg_length, post_msg_length)

        for ii, msg in enumerate(latest_messages):
            if ii == 0:
                self.assertEquals(self.genEmail(eml_ii), msg.recipient)
            else:
                self.assertEquals(self.genEmail(usr_ii), msg.recipient)

        # don't need to assure that the messages from Ledger.addDue are correct
        # Those are covered in LedgerTest.py

        if fail == self.BAD_EML:
            self.assertEquals("You are not a user.\nSend 'ledger help' for"
                " assistance.", latest_messages[-1].message)

        if not fail:
            self.assertEquals(self.genEmail(eml_ii),
                latest_messages[-2].recipient)
            self.assertEquals(self.genEmail(usr_ii),
                latest_messages[-1].recipient)
            self.assertEquals(latest_messages[-1].message,
                latest_messages[-2].message)

    def addLedgerCommand(self, email, command, success=True):
        pre_length = len(self.ledger.command_queue)
        self.ledger.parseLedgerCommand(email, command)
        post_length = len(self.ledger.command_queue)

        if success:
            pre_length += 1

        self.assertEquals(post_length, pre_length)

