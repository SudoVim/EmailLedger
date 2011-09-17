from testing.LedgerTest import LedgerTest
from testing.LedgerTest import User
import unittest

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
