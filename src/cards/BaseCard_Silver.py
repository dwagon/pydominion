import Game
import Card


class Card_Silver(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.DOMINION
        self.desc = "+2 coin"
        self.playable = False
        self.basecard = True
        self.name = 'Silver'
        self.coin = 2
        self.cost = 3
        self.numcards = 40

# EOF
