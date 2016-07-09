

###############################################################################
class LandmarkPile(object):
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.landmark = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.landmark, name)

    ###########################################################################
    def __repr__(self):
        return "Landmark %s" % self.name

# EOF
