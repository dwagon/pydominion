

###############################################################################
class EventPile(object):
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.event = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.event, name)

    ###########################################################################
    def __repr__(self):
        return "Event %s" % self.name

# EOF
