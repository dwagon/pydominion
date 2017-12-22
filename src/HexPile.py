

###############################################################################
class HexPile(object):
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.hx = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.hx, name)

    ###########################################################################
    def __repr__(self):
        return self.name

# EOF
