from testing.commands.CommandTest import CommandTest

class AddMeTest(CommandTest):

    def test_success(self):
        self.addMe(0, 0)

    def test_sameUname(self):
        self.addMe(0, 0)
        self.addMe(1, 0, success=False, fail_uname=True)

    def test_sameEmail(self):
        self.addMe(0, 0)
        self.addMe(0, 1, success=False, fail_uname=False)

