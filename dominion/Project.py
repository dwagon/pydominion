""" https://wiki.dominionstrategy.com/index.php/Project"""
from dominion import Card


class Project(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.PROJECT


# EOF
