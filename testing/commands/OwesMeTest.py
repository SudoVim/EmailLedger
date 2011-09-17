from testing.commands.CommandTest import CommandTest

class OwesMeTest(CommandTest):

    def test_success(self):
        self.addMe(0, 0)
        self.addMe(1, 1)

        self.owesMe(0, 1)

    def test_successIPaid(self):
        self.addMe(0, 0)
        self.addMe(1, 1)

        self.owesMe(0, 1, owes_me=False)

    def test_badEmail(self):
        self.addMe(0, 0)
        self.addMe(1, 1)

        self.owesMe(2, 1, fail=self.BAD_EML)

    def test_badUname(self):
        self.addMe(0, 0)
        self.addMe(1, 1)

        self.owesMe(0, 2, fail=self.BAD_TARGET)
