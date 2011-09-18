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
