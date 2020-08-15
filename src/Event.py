from Card import Card


###############################################################################
class Event(Card):
    pass


###############################################################################
class EventPile(object):
    """ Pile of Events but events are only singletons
        Here so Game code can treat every card type like a pile of cards """
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
