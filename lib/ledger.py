import os

class User(object):
    username = ""
    email = ""

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Due(object):
    ower = None
    owee = None
    ammount = 0

    def __init__(self, ower, owee, ammount):
        self.ower = ower
        self.owee = owee
        self.ammount = float(ammount)

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
            ower, owee, ammount = line.split()
            self.dues.append(Due(ower, owee, ammount))

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
                                                 due.ammount))

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

    def addDue(self, ower, owee, ammount):
        st, ower = self.existsUser(ower)
        if not st:
            return False, ower

        st, owee = self.existsUser(owee)
        if not st:
            return False, owee

        if ammount < 0:
            return False, "A negative ammount cannot be paid!"

        for ii, due in enumerate(self.dues):
            if due.ower == ower and due.owee == owee:
                due.ammount += float(ammount)
                due.ammount = int(due.ammount * 100 + 0.5) / 100.0
                return True, "Dued ammount updated. " \
                             "%s now owes %s $%.2f." \
                             % (due.ower, due.owee, due.ammount)
            elif due.ower == owee and due.owee == ower:
                new_ammount = due.ammount - float(ammount)
                new_ammount = int(new_ammount * 100 + 0.5) / 100.0
                if new_ammount == 0:
                    del self.dues[ii]
                    return True, "%s is now squared on his debt to %s." \
                                 % (owee, ower)
                elif new_ammount < 0:
                    self.dues.append(Due(ower, owee, -1 * new_ammount))
                    del self.dues[ii]
                    return True, "The tables have turned! %s now owes %s " \
                                 "$%.2f." % (ower, owee, -1 * new_ammount)
                else:
                    due.ammount = new_ammount
                    
                    return True, "Some of %s's debt has been paid. %s now " \
                                 "owes %s $%.2f." % (owee, owee, ower,
                                                    new_ammount)

        self.dues.append(Due(ower, owee, ammount))
        return True, "%s now owes %s $%.2f." % (ower, owee, ammount)

    def listUsers(self):
        ret = "Users:\n"
        for user in self.users:
            ret += user.username + "\n"

        return ret

    def listDues(self, user):
        ret = "People who you owe:\n"
        for due in self.dues:
            if due.ower.lower() == user.lower():
                ret += "You owe %s $%.2f\n" % (due.owee, due.ammount)

        ret += "\n"
        ret += "People who owe you:\n"
        for due in self.dues:
            if due.owee.lower() == user.lower():
                ret += "%s owes you $%.2f\n" % (due.ower, due.ammount)

        return ret

