""" http://wiki.dominionstrategy.com/index.php/Trait """
from typing import Any, Optional

from dominion import Card


###############################################################################
class Trait(Card.Card):
    """Class representing traits - mostly just card code"""

    def __init__(self, cardname: Optional[str] = None, klass=None) -> None:
        self.card_pile: Optional[
            Card.Card
        ] = None  # Which card pile this trait is associated with
        Card.Card.__init__(self)
        if cardname:
            self.name = cardname

    ###########################################################################
    def __repr__(self) -> str:
        return f"Trait {self.name}"


###############################################################################
class TraitPile:
    """Pile of Traits but traits are only singletons
    Here so Game code can treat every card type like a pile of cards"""

    def __init__(self, cardname: str, klass) -> None:
        self.cardname = cardname
        self.trait = klass()

    ###########################################################################
    def __getattr__(self, name: str) -> Any:
        return getattr(self.trait, name)


# EOF
