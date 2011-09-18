from testing.commands.CommandTest import CommandTest

class AddEmailTest(CommandTest):

    def test_success(self):
        self.addMe(0, 0)
        self.addEmail(0, 1, 0)

    def test_failEmail(self):
        self.addMe(0, 0)
        self.addEmail(0, 1, 0, fail=self.HAS_EML)

    def test_failOwnEmail(self):
        self.addMe(0, 0)
        self.addMe(1, 1)
        self.addEmail(0, 0, 0, fail=self.BAD_EML)
