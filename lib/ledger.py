import os

class User(object):
    username = ""
    email = ""

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
    ower = None
    owee = None
    amount = 0

    def __init__(self, ower, owee, amount):
        self.ower = ower
        self.owee = owee
        self.amount = float(amount)

    def __eq__(self, other):
        if isinstance(other, Due):
            return self.ower == other.ower and \
                    self.owee == other.owee and \
                    self.ammount == other.ammount
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other)
        if ret is NotImplemented:
            return ret
        return not ret

class Ledger(object):
    DATA_PATH = os.path.join('.','data')
    LEDGER_PATH = os.path.join(DATA_PATH, 'ledger.txt')
    USER_PATH = os.path.join(DATA_PATH, 'users.txt')

    users = []
    dues = []

    def __init__(self):
        try:
            os.mkdir(self.DATA_PATH)
        except:
            pass

        for path in [self.LEDGER_PATH, self.USER_PATH]:
            if not os.path.exists(path):
                open(path, 'w').close()

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
            ledger_file.write("%s %s %0.2f\n" % (due.ower, due.owee,
                                                 due.amount))

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
        st, ower = self.existsUser(ower)
        if not st:
            return False, ower

        st, owee = self.existsUser(owee)
        if not st:
            return False, owee

        if amount < 0:
            return False, "A negative amount cannot be paid!"

        for ii, due in enumerate(self.dues):
            if due.ower == ower and due.owee == owee:
                due.amount += float(amount)
                due.amount = int(due.amount * 100 + 0.5) / 100.0
                return True, "Dued amount updated. " \
                             "%s now owes %s $%.2f." \
                             % (due.ower, due.owee, due.amount)
            elif due.ower == owee and due.owee == ower:
                new_amount = due.amount - float(amount)
                new_amount = int(new_amount * 100 + 0.5) / 100.0
                if new_amount == 0:
                    del self.dues[ii]
                    return True, "%s is now squared on his debt to %s." \
                                 % (owee, ower)
                elif new_amount < 0:
                    self.dues.append(Due(ower, owee, -1 * new_amount))
                    del self.dues[ii]
                    return True, "The tables have turned! %s now owes %s " \
                                 "$%.2f." % (ower, owee, -1 * new_amount)
                else:
                    due.amount = new_amount
                    
                    return True, "Some of %s's debt has been paid. %s now " \
                                 "owes %s $%.2f." % (owee, owee, ower,
                                                    new_amount)

        self.dues.append(Due(ower, owee, amount))
        return True, "%s now owes %s $%.2f." % (ower, owee, amount)

    def listUsers(self):
        ret = "Users:\n"
        for user in self.users:
            ret += user.username + "\n"

        return ret

    def listDues(self, user):
        ret = "People who you owe:\n"
        for due in self.dues:
            if due.ower.lower() == user.lower():
                ret += "You owe %s $%.2f\n" % (due.owee, due.amount)

        ret += "\n"
        ret += "People who owe you:\n"
        for due in self.dues:
            if due.owee.lower() == user.lower():
                ret += "%s owes you $%.2f\n" % (due.ower, due.amount)

        return ret

