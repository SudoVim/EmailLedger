import unittest
import shutil
import os
import random

from lib.Ledger import Ledger

class LedgerTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(Ledger.DATA_PATH):
            shutil.rmtree(Ledger.DATA_PATH)

        self.ledger = Ledger()
        self.num_users = 0
        self.test_uname = "testuname"
        self.test_email = "testemail"

    def genUsername(self, ii):
        return "%s%d" % (self.test_uname, ii)

    def genEmail(self, ii):
        return "%s%d" % (self.test_email, ii)

    def addUser(self):
        return self.ledger.addUser(self.genUsername(self.num_users),
                            self.genEmail(self.num_users))
        self.num_users += 1

    def assertUsersCorrect(self):
        self.assertEquals(len(self.ledger.users), self.num_users)
        for ii, user in enumerate(self.ledger.users):
            self.assertEquals(self.ledger.users[ii].username,
                              self.genUsername(ii))
            self.assertEquals(self.ledger.users[ii].email,
                              self.genEmail(ii))

    def addDue(ower_idx, owee_idx, ammount):
        return self.ledger.addDue(self.users[ower_idx].username,
                           self.users[owee_idx].username,
                           ammount)

class AddUserTest(LedgerTest):

    # Success case(s)
    def test_addUsers(self):
        test_users = 5

        # Make sure users are added correctly
        for ii in range(test_users):
            st, msg = self.addUser()
            self.assertEquals(st, True)
            self.assertEquals(msg, "Successfully added user %s with email "
                              "%s." % (self.genUsername(ii), self.genEmail(ii))
            self.assertUsersCorrect(self)

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

class AddDueTest(LedgerTest):

    def getRandomTestIter(self):
        return random.randint(2, 10)

    def getRandomDueIncrement(self):
        return int(random.random() * 3 * 100) / 100.0

    # Success case(s)
    def test_addDues(self):
        test_iters = self.getRandomTestIter()
        due_increment = self.getRandomDueIncrement()

        # add two users
        for ii in range(2):
            self.addUser()

        for ii in range(test_iters):
            st, msg = self.addDue(0, 1, due_increment)
            self.assertEquals(len(self.dues), 1)
            self.assertEquals(self.dues[0], Due(self.genUsername(0),
                                                self.genUsername(1),
                                                due_increment * (ii + 1))
            self.assertEquals(st, True)
            self.assertEquals(msg, "%s now owes %s $%.2f."
                % (self.genUsername(0), self.genUsername(1),
                    (ii + 1) * due_increment))

    def test_reduceDue(self):
        test_iters = self.getRandomTestIter()
        due_increment = self.getRandomDueIncrement()

        # add two users
        for ii in range(2):
            self.addUser()

        self.addDue(0, 1, test_iters)
        for ii in range(test_iters):
            st, msg = self.addDue(1, 0, due_increment)
            self.assertEquals(len(self.dues), 1)
            self.assertEquals(seld.dues[0], Due(self.genUsername(0),
                                                self.genUsername(1),
                                                (test_iters - ii - 1) *
                                                due_increment))
            self.assertEquals(st, True)

            if test_iters - ii > 1:
                self.assertEquals(msg, "Dued ammount updated. %s now owes %s "
                                       "$%.2f." % (self.genUsername(0),
                                                   self.genUsername(1),
                                                   (test_iters - ii - 1) *
                                                   due_increment))
