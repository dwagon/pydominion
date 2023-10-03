""" http://wiki.dominionstrategy.com/index.php/Trait """
from dominion import Card


###############################################################################
class Trait(Card.Card):
    """Class representing traits - mostly just card code"""

    def __init__(self, cardname=None, klass=None):
        self.card_pile = None  # Which card pile this trait is associated with
        Card.Card.__init__(self)
        self.name = cardname

    ###########################################################################
    def __repr__(self):
        return f"Trait {self.name}"


###############################################################################
class TraitPile:
    """Pile of Traits but traits are only singletons
    Here so Game code can treat every card type like a pile of cards"""

    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.trait = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.trait, name)


# EOF
