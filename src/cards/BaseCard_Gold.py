import Game
import Card


class Card_Gold(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.DOMINION
        self.desc = "+3 coin"
        self.playable = False
        self.basecard = True
        self.name = 'Gold'
        self.coin = 3
        self.cost = 6
        self.numcards = 30

# EOF
