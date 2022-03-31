""" http://wiki.dominionstrategy.com/index.php/Event """
from dominion import Card


###############################################################################
class Event(Card.Card):
    """Class representing events - mostly just card code"""


###############################################################################
class EventPile:
    """Pile of Events but events are only singletons
    Here so Game code can treat every card type like a pile of cards"""

    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.event = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.event, name)

    ###########################################################################
    def __repr__(self):
        return f"Event {self.name}"


# EOF
