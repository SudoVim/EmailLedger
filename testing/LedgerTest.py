import unittest
import shutil
import os
import random

from lib.Ledger import Ledger
from lib.Due import Due
from lib.User import User

class LedgerTest(unittest.TestCase):
    test_uname = "testuname"
    test_email = "testemail"

    def setUp(self):
        self.ledger = Ledger()
        self.num_users = 0

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

    def addEmail(self, usr_ii, eml_ii):
        return self.ledger.addEmail(self.genUsername(usr_ii),
            self.genEmail(eml_ii))

    def removeEmail(self, usr_ii, eml_ii):
        return self.ledger.removeEmail(self.genUsername(usr_ii),
            self.genEmail(eml_ii))

    def assertUsersCorrect(self):
        self.assertEquals(len(self.ledger.users), self.num_users)
        for ii, user in enumerate(self.ledger.users):
            self.assertEquals(self.ledger.users[ii].username,
                              self.genUsername(ii))
            self.assertEquals(self.ledger.users[ii].email[0],
                              self.genEmail(ii))

    def addDue(self, ower_idx, owee_idx, amount):
        return self.ledger.addDue(self.ledger.users[ower_idx].username,
                           self.ledger.users[owee_idx].username,
                           amount)

