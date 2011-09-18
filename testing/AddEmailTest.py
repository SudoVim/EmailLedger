from testing.LedgerTest import LedgerTest

class AddEmailTest(LedgerTest):

    def test_success(self):
        self.addUser()

        st, msg = self.addEmail(0, 1)
        self.assertEquals(True, st)
        self.assertEquals("Email address %s successfully added to user %s."
            % (self.genEmail(1), self.genUsername(0)), msg)

        self.assertEquals(len(self.ledger.users[0].email), 2)

    def test_badUser(self):
        self.addUser()

        st, msg = self.addEmail(1, 1)
        self.assertEquals(False, st)
        self.assertEquals("%s doesn't exist." % self.genUsername(1), msg)

        self.assertEquals(len(self.ledger.users[0].email), 1)

    def test_inUseEmail(self):
        self.addUser()
        self.addUser()

        st, msg = self.addEmail(0, 1)
        self.assertEquals(False, st)
        self.assertEquals("Email address %s is in use by another user."
            % self.genEmail(1), msg)

        self.assertEquals(len(self.ledger.users[0].email), 1)

    def test_youUseEmail(self):
        self.addUser()

        st, msg = self.addEmail(0, 0)
        self.assertEquals(False, st)
        self.assertEquals("Email address %s is already connected to your "
            "account." % self.genEmail(0), msg)

        self.assertEquals(len(self.ledger.users[0].email), 1)
