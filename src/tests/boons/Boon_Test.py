from Boon import Boon


###############################################################################
class Boon_Test(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = "boon"
        self.desc = "Test Boon"
        self.base = "TEST"
        self.name = "TestBoon"


# EOF
