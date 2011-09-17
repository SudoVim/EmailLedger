from testing.LedgerTest import LedgerTest
from testing.LedgerTest import Due
import random

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
