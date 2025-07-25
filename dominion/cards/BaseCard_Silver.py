import dominion.Card as Card


class Card_Silver(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+2 coin"
        self.playable = False
        self.basecard = True
        self.name = "Silver"
        self.coin = 2
        self.cost = 3
        self.numcards = 40


# EOF
