import os

class User(object):

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __eq__(self, other):
        if isinstance(other, User):
            return self.username == other.username and \
                    self.email == other.email
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other)
        if ret is NotImplemented:
            return ret
        return not ret

class Due(object):

    def __init__(self, ower, owee, amount):
        self.ower = ower
        self.owee = owee
        self.amount = int(amount)

    def formatAmount(self):
        return "%d.%02d" % (self.amount / 100, self.amount % 100)

    def __eq__(self, other):
        if isinstance(other, Due):
            return self.ower == other.ower and \
                    self.owee == other.owee and \
                    self.amount == other.amount
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other)
        if ret is NotImplemented:
            return ret
        return not ret

    def __str__(self):
        return "ower: %s owee: %s amount: %s" % (self.ower, self.owee,
            self.formatAmount())

class Ledger(object):
    DATA_PATH = os.path.join('.','data')
    LEDGER_PATH = os.path.join(DATA_PATH, 'ledger.txt')
    USER_PATH = os.path.join(DATA_PATH, 'users.txt')

    def __init__(self):
        try:
            os.mkdir(self.DATA_PATH)
        except:
            pass

        for path in [self.LEDGER_PATH, self.USER_PATH]:
            if not os.path.exists(path):
                open(path, 'w').close()

        self.users = []
        self.dues = []

    def readUsers(self):
        self.users = []
        users_file = open(self.USER_PATH, 'r')
        lines = users_file.readlines()
        users_file.close()

        for line in lines:
            name, email = line.split()
            self.users.append(User(name, email))

    def sortUsers(self):
        for ii in xrange(1, len(self.users)):
            for jj in xrange(ii - 1, 0, -1):
                if self.users[jj].username.lower() < \
                        self.users[jj - 1].username.lower():
                    self.users[jj], self.users[jj - 1] = \
                            self.users[jj - 1], self.users[jj]

    def readLedger(self):
        self.dues = []
        ledger_file = open(self.LEDGER_PATH, 'r')
        lines = ledger_file.readlines()
        ledger_file.close()

        for line in lines:
            ower, owee, amount = line.split()
            amount = int(float(amount) * 100 + .5)
            self.dues.append(Due(ower, owee, amount))

    def dumpUsers(self):
        users_file = open(self.USER_PATH, 'w')

        self.sortUsers()

        for user in self.users:
            users_file.write("%s %s\n" % (user.username, user.email))

        users_file.close()

    def dumpLedger(self):
        ledger_file = open(self.LEDGER_PATH, 'w')

        for due in self.dues:
            ledger_file.write("%s %s %s\n" % (due.ower, due.owee,
                                                 due.formatAmount()))

        ledger_file.close()

    def addUser(self, username, email):
        for user in self.users:
            if username.lower() == user.username.lower():
                return False, "Username '%s' already exists for another user."\
                              % (username)

            if email.lower() == user.email.lower():
                return False, "Email '%s' already exists for another user." \
                              % (email)

        self.users.append(User(username, email))
        return True, "Successfully added user %s with email %s." \
                     % (username, email)

    def existsUser(self, user):
        for usr in self.users:
            if user.lower() == usr.username.lower():
                return True, usr.username

        return False, "%s doesn't exist." % user

    def getUnameFromEmail(self, email):
        for user in self.users:
            if user.email.lower() == email.lower():
                return True, user.username

        return False, None

    def getEmailFromUname(self, uname):
        for user in self.users:
            if user.username.lower() == uname.lower():
                return True, user.email

        return False, None

    def addDue(self, ower, owee, amount):
        amount = int(float(amount) * 100 + .5)
        st, ower = self.existsUser(ower)
        if not st:
            return False, ower

        st, owee = self.existsUser(owee)
        if not st:
            return False, owee

        if amount < 0:
            return False, "A negative amount cannot be paid!"

        for ii, due in enumerate(self.dues):
            if due.ower.lower() == ower.lower() and \
                    due.owee.lower() == owee.lower():
                due.amount += amount
                return True, "Dued amount updated. " \
                             "%s now owes %s $%s." \
                             % (due.ower, due.owee, due.formatAmount())
            elif due.ower.lower() == owee.lower() and \
                    due.owee.lower() == ower.lower():
                new_amount = due.amount - amount
                if new_amount == 0:
                    del self.dues[ii]
                    return True, "%s is now squared on his debt to %s." \
                                 % (owee, ower)
                elif new_amount < 0:
                    new_due = Due(ower, owee, -1 * new_amount)
                    self.dues.append(new_due)
                    del self.dues[ii]
                    return True, "The tables have turned! %s now owes %s " \
                                 "$%s." % (ower, owee, new_due.formatAmount())
                else:
                    due.amount = new_amount
                    
                    return True, "Some of %s's debt has been paid. %s now " \
                                 "owes %s $%s." % (owee, owee, ower,
                                                    due.formatAmount())

        new_due = Due(ower, owee, amount)
        self.dues.append(new_due)
        return True, "%s now owes %s $%s." % (ower, owee, new_due.formatAmount())

    def listUsers(self):
        ret = "Users:\n"
        for user in self.users:
            ret += user.username + "\n"

        return ret

    def listDues(self, user):
        ret = "People who you owe:\n"
        for due in self.dues:
            if due.ower.lower() == user.lower():
                ret += "You owe %s $%s\n" % (due.owee, due.formatAmount())

        ret += "\n"
        ret += "People who owe you:\n"
        for due in self.dues:
            if due.owee.lower() == user.lower():
                ret += "%s owes you $%s\n" % (due.ower, due.formatAmount())

        return ret

