import dominion.Game as Game
import dominion.Card as Card


class Card_Potion(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.ALCHEMY
        self.basecard = True
        self.playable = False
        self.desc = "+1 potion"
        self.name = "Potion"
        self.potion = 1
        self.cost = 4


# EOF
