from testing.commands.CommandTest import CommandTest

class AddMeTest(CommandTest):

    def test_success(self):
        self.addMe(0, 0)

    def test_sameUname(self):
        self.addMe(0, 0)
        self.addMe(1, 0, fail=self.BAD_UNAME)

    def test_sameEmail(self):
        self.addMe(0, 0)
        self.addMe(0, 1, fail=self.BAD_EML)

