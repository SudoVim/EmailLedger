class User(object):

    def __init__(self, username, email):
        self.username = username

        if isinstance(email, list):
            self.email = email
        else:
            self.email = []
            self.email.append(email)

    def removeEmail(self, email):
        for ii, eml in enumerate(self.email):
            if email == eml:
                if len(self.email) == 1:
                    return False, "Cannot remove your only email."
                del self.email[ii]
                return True, "Removed email address %s from account %s." \
                    % (email, self.username)

        return False, "You do not have an email %s linked to your account." \
            % email

    def listEmails(self):
        ret = "Attached Emails:\n"
        for eml in self.email:
            ret += eml + "\n"

        return True, ret

    def __eq__(self, other):
        if isinstance(other, User):
            if self.username == other.username and \
                    len(self.email) == len(other.email):
                for eml1, eml2 in zip(self.email, other.email):
                    if eml1 != eml2:
                        return False

                return True
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other)
        if ret is NotImplemented:
            return ret
        return not ret

    def printLine(self):
        ret = self.username
        for eml in self.email:
            ret += " " + eml

        return ret
