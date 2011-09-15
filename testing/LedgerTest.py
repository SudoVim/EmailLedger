import unittest
import shutil
import os
import random

from lib.ledger import Ledger
from lib.ledger import Due
from lib.ledger import User

class LedgerTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(Ledger.DATA_PATH):
            shutil.rmtree(Ledger.DATA_PATH)

        self.ledger = Ledger()
        self.ledger.users = []
        self.ledger.dues = []
        self.num_users = 0
        self.test_uname = "testuname"
        self.test_email = "testemail"

    def genUsername(self, ii):
        return "%s%d" % (self.test_uname, ii)

    def genDue(self, ower_idx, owee_idx, amount):
        return Due(self.genUsername(ower_idx), self.genUsername(owee_idx),
                   int(amount * 100 + .5))

    def genEmail(self, ii):
        return "%s%d" % (self.test_email, ii)

    def addUser(self):
        st, msg = self.ledger.addUser(self.genUsername(self.num_users),
                            self.genEmail(self.num_users))
        self.num_users += 1

        return st, msg

    def assertUsersCorrect(self):
        self.assertEquals(len(self.ledger.users), self.num_users)
        for ii, user in enumerate(self.ledger.users):
            self.assertEquals(self.ledger.users[ii].username,
                              self.genUsername(ii))
            self.assertEquals(self.ledger.users[ii].email,
                              self.genEmail(ii))

    def addDue(self, ower_idx, owee_idx, amount):
        return self.ledger.addDue(self.ledger.users[ower_idx].username,
                           self.ledger.users[owee_idx].username,
                           amount)

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

class AddDueTest(LedgerTest):

    def getRandomTestIter(self):
        return random.randint(2, 10)

    def getRandomDueIncrement(self):
        return random.randint(1, 299) / 100.0

    # Success case(s)
    def test_addDues(self):
        test_iters = self.getRandomTestIter()
        due_increment = self.getRandomDueIncrement()

        # add two users
        for ii in range(2):
            self.addUser()

        for ii in range(test_iters):
            st, msg = self.addDue(0, 1, due_increment)
            self.assertEquals(len(self.ledger.dues), 1)
            self.assertEquals(self.ledger.dues[0], Due(self.genUsername(0),
                                                self.genUsername(1),
                                                int(due_increment * (ii + 1) *
                                                100 + .5)))
            self.assertEquals(st, True)

            if ii == 0:
                self.assertEquals(msg, "%s now owes %s $%.2f."
                    % (self.genUsername(0), self.genUsername(1),
                        (ii + 1) * due_increment))
            else:
                self.assertEquals(msg, "Dued amount updated. %s now owes %s "
                    "$%.2f." % (self.genUsername(0), self.genUsername(1),
                    (ii + 1) * due_increment))

    def test_reduceDue(self):
        test_iters = self.getRandomTestIter()
        due_increment = self.getRandomDueIncrement()

        # add two users
        for ii in range(2):
            self.addUser()

        self.addDue(0, 1, due_increment * test_iters)
        for ii in range(test_iters):
            st, msg = self.addDue(1, 0, due_increment)
            self.assertEquals(len(self.ledger.dues), 1 if ii < test_iters - 1 \
                                                     else 0)

            if ii == test_iters - 1:
                break

            new_due = self.genDue(0, 1, (test_iters - ii - 1) * due_increment)
            self.assertEquals(self.ledger.dues[0], new_due)
            self.assertEquals(st, True)

            self.assertEquals(msg, "Some of %s's debt has been paid. %s "
                                   "now owes %s $%s."
                                   % (self.genUsername(0),
                                   self.genUsername(0),
                                   self.genUsername(1),
                                   new_due.formatAmount()))

    def test_paidBackMore(self):
        due_increment = self.getRandomDueIncrement()

        # add two users
        for ii in range(2):
            self.addUser()

        self.addDue(0, 1, due_increment)

        st, msg = self.addDue(1, 0, 2 * due_increment)
        self.assertEquals(len(self.ledger.dues), 1)

        new_due = self.genDue(1, 0, due_increment)
        self.assertEquals(self.ledger.dues[0], new_due)

        self.assertEquals(st, True)
        self.assertEquals(msg, "The tables have turned! %s now owes %s $%s."
                               % (self.genUsername(1), self.genUsername(0),
                                  new_due.formatAmount()))

class UserTest(unittest.TestCase):

    TEST_UNAME = "uname"
    TEST_EMAIL = "email"

    def makeUser(self, usr_idx, eml_idx):
        return User("%s%d" % (self.TEST_UNAME, usr_idx),
                    "%s%d" % (self.TEST_EMAIL, eml_idx))

    def test_UserEq(self):
        uname_lista = [0, 0, 0, 0]
        email_lista = [0, 0, 0, 0]

        uname_listb = [0, 0, 1, 1]
        email_listb = [0, 1, 0, 1]

        eq_result = [True, False, False, False]
        ne_result = [False, True, True, True]

        for ua, ea, ub, eb, er, nr in zip(uname_lista, email_lista,
            uname_listb, email_listb, eq_result, ne_result):
            usr1 = self.makeUser(ua, ea)
            usr2 = self.makeUser(ub, eb)

            self.assertEquals(usr1 == usr2, er)
            self.assertEquals(usr1 != usr2, nr)

