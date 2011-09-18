from testing.LedgerTest import LedgerTest

class RemoveEmailTest(LedgerTest):

    def test_success(self):
        self.addUser()
        self.addEmail(0, 1)
        pre_eml_length = len(self.ledger.users[0].email)

        st, msg = self.removeEmail(0, 1)
        post_eml_length = len(self.ledger.users[0].email)

        self.assertEquals(st, True)
        self.assertEquals(pre_eml_length - 1, post_eml_length)
        self.assertEquals(msg, "Removed email address %s from account %s."
            % (self.genEmail(1), self.genUsername(0)))

    def test_onlyEmail(self):
        self.addUser()
        pre_eml_length = len(self.ledger.users[0].email)

        st, msg = self.removeEmail(0, 0)
        post_eml_length = len(self.ledger.users[0].email)

        self.assertEquals(st, False)
        self.assertEquals(pre_eml_length, post_eml_length)
        self.assertEquals(msg, "Cannot remove your only email.")

    def test_noHasEmail(self):
        self.addUser()
        pre_eml_length = len(self.ledger.users[0].email)

        st, msg = self.removeEmail(0, 1)
        post_eml_length = len(self.ledger.users[0].email)

        self.assertEquals(st, False)
        self.assertEquals(pre_eml_length, post_eml_length)
        self.assertEquals(msg, "You do not have an email %s linked to your"
            " account." % self.genEmail(1))

