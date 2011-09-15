#!/usr/bin/python
import smtplib
import os
import re

from lib.ledger import Ledger
import lib.functions

from poplib import POP3_SSL

# Import the email modules we'll need
from email.mime.text import MIMEText
import email

class Message(object):
    recipient = ""
    message = ""

    def __init__(recpient, message):
        self.recipient = recipient
        self.message = message

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.recipient == other.recipient and \
                self.message == other.message
        return NotImplemented

    def __ne__(self, other):
        ret = self.__eq__(other):
        if ret is NotImplemented:
            return ret
        return not ret

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
    ledger = None
    mail_server = ""
    port = ""
    username = ""
    password = ""

    from_regex = ".*<(.*)>.*"

    command_queue = []
    message_list = []

    debug_mode = False

    def __init__(self, mail_server, port, username, password):
        super(EmailLedgerInterface, self).__init__()

        self.mail_server = mail_server
        self.port = port
        self.username = username
        self.password = password

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
                            if self.parseLedgerCommand(line):
                                ledger_command_received = True
                                print "Received command: %s from %s" \
                                        % (line,  sender)

                if not ledger_command_received:
                    sendMessage(sender, "You must begin each command with "
                                        "'ledger'")

        pop_client.quit()

    def parseLedgerCommand(self, command):
        split = command.split()

        # find the command line
        if len(split) > 0:
            if split[0].lower() == "ledger":
                self.command_queue.append(Command(line,
                                    sender, split[1:]))
                return True

        return False
           
    def performCommands(self):
        for command in self.command_queue:
            args = command.args

            # help
            if len(args) >= 1 and args[0].lower() == "help":
                self.sendMessage(command.issuer,
                        "Commands:\n"
                        "add me <uname>\n"
                        "<uname> owes me <amount>\n"
                        "i paid <uname> <amount>\n"
                        "get users\n"
                        "get my dues\n"
                        "help\n"
                        "\n"
                        "Remember: Always put 'ledger' in the subject line "
                        "and before each command. Also, usernames must be a "
                        "single token. (no spaces)\n"
                        "\n"
                        "eg. ledger add me my_name\n"
                        "\n"
                        "And of course... https://github.com/SudoVim/TMSLedger\n")
                continue

            # add me <uname>
            if len(args) >= 3 and ("%s %s" % (args[0], args[1])).lower() \
                    == "add me":
                if not self.addUser(args[2], command.issuer):
                    self.sendMessage(command.issuer, "%s: Username or email "
                                                     "address already exists"
                                                     % command.command)
                    continue

                self.sendMessage(command.issuer, "Username %s added with "
                                                 "address %s"
                                                 % (args[2], command.issuer))
                continue

            # <uname> owes me <amount>
            if len(args) >= 4 and ("%s %s" % (args[1], args[2])).lower() \
                    == "owes me":
                st, owee = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.sendMessage(command.issuer, "you are not a user.\n"
                                                     "send 'ledger help' for"
                                                     " assistance")
                    continue

                ower = args[0]
                amount = float(args[3].strip("$"))

                st, msg = self.addDue(ower, owee, amount)
                if not st:
                    self.sendMessage(command.issuer, msg)
                    continue

                self.sendMessage(command.issuer, msg)
                self.sendMessage(self.getEmailFromUname(ower)[1], msg)
                continue

            # i paid <uname> <amount>
            if len(args) >= 4 and ("%s %s" % (args[0], args[1])).lower() == \
                    "i paid":
                owee = args[2]
                st, ower = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.sendMessage(command.issuer, "you are not a user.\n"
                                                     "send 'ledger help' for"
                                                     " assistance")
                    continue

                amount = float(args[3].strip("$"))

                st, msg = self.addDue(owee, ower, amount)
                if not st:
                    self.sendMessage(command.issuer, msg)
                    continue

                self.sendMessage(command.issuer, msg)
                self.sendMessage(self.getEmailFromUname(owee)[1], msg)
                continue

            # get users
            if len(args) >= 2 and ("%s %s" % (args[0], args[1])).lower() \
                    == "get users":
                self.sendMessage(command.issuer, self.listUsers())
                continue

            # get my dues
            if len(args) >= 3 and ("%s %s %s" % (args[0], args[1], \
                    args[2])).lower() == "get my dues":
                st, user = self.getUnameFromEmail(command.issuer)
                if not st:
                    self.sendMessage(command.issuer, "you are not a user.\n"
                                                     "send 'ledger help' for"
                                                     " assistance")
                    continue

                self.sendMessage(command.issuer, self.listDues(user))
                continue

            self.sendMessage(command.issuer, "%s: I didn't understand you. "
                                             "Send 'ledger help' for "
                                             "assistance" % command.command)

        self.dumpUsers()
        self.dumpLedger()
        self.command_queue = []

    def sendMessage(self, to_address, message):
        self.message_list.append(Message(to_address, message))
        if self.debug_mode:
            return

        # From http://docs.python.org/library/email-examples.html
        # Create a text/plain message
        msg = MIMEText(message)
        me = "%s@gmail.com" % self.username
        you = to_address

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
        server.sendmail('%s@gmail.com' % self.username,to_address,
                        msg.as_string())
        server.close()
            

