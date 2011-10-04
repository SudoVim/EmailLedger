#!/usr/bin/python
import smtplib
import os
import re

from lib.Ledger import Ledger
import lib.functions

from poplib import POP3_SSL

# Import the email modules we'll need
from email.mime.text import MIMEText
import email

class Message(object):
    recipient = ""
    message = ""

    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.recipient == other.recipient and \
                self.message == other.message
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other)
        if ret is NotImplemented:
            return ret
        return not ret

    def __str__(self):
        return "To: %s; Message: %s" % (self.recipient, self.message)

class Command(object):
    command = ""
    args = []
    issuer = None
    issuee = None

    def __init__(self, command, issuer, args, issuee=None):
        self.command = command
        self.issuer = issuer
        self.args = args
        self.issuee = issuee

    def __str__(self):
        return "command: %s, args: %s, issuer: %s" \
                % (command, args, issuer)

class EmailLedgerInterface(Ledger):
    from_regex = ".*<(.*)>.*"

    debug_mode = False

    def __init__(self, mail_server, port, username, password):
        super(EmailLedgerInterface, self).__init__()

        self.mail_server = mail_server
        self.port = port
        self.username = username
        self.password = password

        self.command_queue = []
        self.message_list = []

    def receiveCommands(self):
        pop_client = POP3_SSL(self.mail_server, self.port)
        pop_client.user(self.username)
        pop_client.pass_(self.password)

        total_messages = len(pop_client.list()[1])
        if total_messages > 0:
            for ii in xrange(1, total_messages + 1):
                headers = email.message_from_string(lib.functions.listToStr(
                                                    pop_client.retr(ii)[1]))
                sender = ""

                print "Received email: %s" % headers['subject']

                # check if it's a ledger email
                if 'ledger' not in headers['subject'].lower():
                    continue

                print "it's a ledger email"

                # parse out who the email is from
                m = re.match(self.from_regex, headers['from'])
                if m:
                    sender = m.group(1)
                else:
                    continue

                print "sender is %s" % sender

                ledger_command_received = False

                for part in headers.walk():
                    if part.get_content_type() == 'text/plain':
                        print part.get_payload()
                        lines = part.get_payload().split('\n')

                        for line in lines:
                            if self.parseLedgerCommand(sender, line):
                                ledger_command_received = True
                                print "Received command: %s from %s" \
                                        % (line,  sender)

                if not ledger_command_received:
                    self.queueMessage(sender, "You must begin each command "
                                        "with 'ledger'")

        pop_client.quit()

    def parseLedgerCommand(self, sender, command):
        split = command.split()

        # find the command line
        if len(split) > 0:
            if split[0].lower() == "ledger":
                self.command_queue.append(Command(command,
                                    sender, split[1:]))
                return True

        return False
           
    def performCommands(self):
        for command in self.command_queue:
            args = command.args

            # help
            if len(args) >= 1 and args[0].lower() == "help":
                self.queueMessage(command.issuer,
                        "Commands:\n"
                        "add me <uname>             - add yourself as a user\n"
                        "add email <email>          - add email address to\n"
                        "                             your account\n"
                        "remove email <email>       - remove <email> from\n"
                        "                             your account\n"
                        "get my emails              - get a list of email\n"
                        "                             addresses attached to\n"
                        "                             your account\n"
                        "<uname> owes me <amount>   - <uname> owes you money\n"
                        "i paid <uname> <amount>    - you paid <uname> some\n"
                        "                           - money\n"
                        "i owe <uname> <amount>     - you owe <uname> money\n"
                        "get users                  - get a list of users\n"
                        "get my dues                - get who you owe and\n"
                        "                             who owes you money\n"
                        "help                       - get this help again\n"
                        "\n"
                        "Remember: Always put 'ledger' in the subject line "
                        "and before each command. Also, usernames must be a "
                        "single token. (no spaces)\n"
                        "\n"
                        "eg. ledger add me my_name\n"
                        "\n"
                        "And of course..."
                        " https://github.com/SudoVim/EmailLedger\n")
                continue

            # add me <uname>
            if len(args) >= 3 and ("%s %s" % (args[0], args[1])).lower() \
                    == "add me":
                st, msg = self.addUser(args[2], command.issuer)
                self.queueMessage(command.issuer, msg)
                continue

            # add email <email>
            if len(args) >= 3 and ("%s %s" % (args[0], args[1])).lower() \
                    == "add email":
                st, uname = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.notAUser(command.issuer)
                    continue

                st, msg = self.addEmail(uname, args[2])

                self.queueMessage(command.issuer, msg)
                continue

            # remove email <email>
            if len(args) >= 3 and ("%s %s" % (args[0], args[1])).lower() \
                    == "remove email":
                st, uname = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.notAUser(command.issuer)
                    continue

                st, msg = self.removeEmail(uname, args[2])

                self.queueMessage(command.issuer, msg)
                continue

            # get my emails
            if len(args) >= 3and ("%s %s %s" % (args[0], args[1],
                    args[2])).lower() == "get my emails":
                st, uname = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.notAUser(command.issuer)
                    continue

                st, msg = self.listEmails(uname)

                self.queueMessage(command.issuer, msg)
                continue

            owesMe = False
            ower = ""
            owee = ""
            st = False
            # <uname> owes me <amount>
            if len(args) >= 4 and ("%s %s" % (args[1], args[2])).lower() \
                    == "owes me":
                ower = args[0]
                st, owee = self.getUnameFromEmail(command.issuer)
                owesMe = True

            # i paid <uname> <amount>
            if len(args) >= 4 and ("%s %s" % (args[0], args[1])).lower() == \
                    "i paid":
                ower = args[2]
                st, owee = self.getUnameFromEmail(command.issuer)
                owesMe = True

            # i owe <uname> <amount>
            if len(args) >= 4 and ("%s %s" % (args[0], args[1])).lower() == \
                    "i owe":
                owee = args[2]
                st, ower = self.getUnameFromEmail(command.issuer)
                owesMe = True

            # 'owes me' and 'i paid' work the same way
            if owesMe:
                if not st:
                    self.notAUser(command.issuer)
                    continue

                amount = float(args[3].strip("$"))

                st, msg = self.addDue(ower, owee, amount)
                self.queueMessage(command.issuer, msg)
                if st:
                    self.queueMessage(self.getEmailFromUname(ower)[1], msg)
                continue

            # get users
            if len(args) >= 2 and ("%s %s" % (args[0], args[1])).lower() \
                    == "get users":
                self.queueMessage(command.issuer, self.listUsers())
                continue

            # get my dues
            if len(args) >= 3 and ("%s %s %s" % (args[0], args[1], \
                    args[2])).lower() == "get my dues":
                st, user = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.notAUser(command.issuer)
                    continue

                self.queueMessage(command.issuer, self.listDues(user))
                continue

            self.queueMessage(command.issuer, "%s: I didn't understand you. "
                                             "Send 'ledger help' for "
                                             "assistance" % command.command)

        self.command_queue = []

    def notAUser(self, to_address):
            self.queueMessage(to_address, "You are not a user.\n"
                "Send 'ledger help' for assistance.")

    def queueMessage(self, to_address, message):
        if isinstance(to_address, list):
            for addr in to_address:
                self.message_list.append(Message(addr, message))
        else:
            self.message_list.append(Message(to_address, message))

    def sendMessages(self):
        if self.debug_mode:
            return

        # sort messages by recipient
        sorted_messages = {}
        for msg in self.message_list:
            try:
                sorted_messages[msg.recipient]
            except KeyError:
                sorted_messages[msg.recipient] = []

            sorted_messages[msg.recipient].append(msg)

        for key in sorted_messages.keys():
            msg_to_send = "--------------------------\n"
            for msg in sorted_messages[key]:
                msg_to_send += msg.message + "\n"
                msg_to_send += "--------------------------\n"

            # From http://docs.python.org/library/email-examples.html
            # Create a text/plain message
            msg = MIMEText(msg_to_send)
            me = "%s@gmail.com" % self.username
            you = key

            # me == the sender's email address
            # you == the recipient's email address
            msg['Subject'] = 'ledger'
            msg['From'] = me
            msg['To'] = you

            server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('%s@gmail.com' % self.username,self.password)
            server.sendmail('%s@gmail.com' % self.username, you,
                            msg.as_string())
            server.close()

        self.message_list = []

