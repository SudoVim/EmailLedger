from testing.LedgerTest import LedgerTest

class AddUserTest(LedgerTest):

    # Success case(s)
    def test_addUsers(self):
        test_users = 5

        # Make sure users are added correctly
        for ii in range(test_users):
            st, msg = self.addUser()
            self.assertEquals(st, True)
            self.assertEquals(msg, "Successfully added user %s with email "
                              "%s." % (self.genUsername(ii),
                              self.genEmail(ii)))
            self.assertUsersCorrect()

    # Failure case(s)
    def test_same_username(self):
        self.addUser()
        self.num_users -= 1
        st, msg = self.addUser()

        self.assertEquals(st, False)
        self.assertEquals(msg, "Username '%s' already exists for another user."
                               % (self.genUsername(0)))

    def test_same_email(self):
        self.addUser()
        st, msg = self.ledger.addUser(
            "%s" % (self.genUsername(self.num_users)),
            "%s" % (self.genEmail(0)))

        self.assertEquals(st, False)
        self.assertEquals(msg, "Email '%s' already exists for another user."
                               % (self.genEmail(0)))
