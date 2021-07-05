###############################################################################
class StatePile(object):
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.boon = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.boon, name)

    ###########################################################################
    def __repr__(self):
        return self.name


# EOF
