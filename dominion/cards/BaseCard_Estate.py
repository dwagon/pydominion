import dominion.Game as Game
import dominion.Card as Card


class Card_Estate(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.DOMINION
        self.desc = "1 VP"
        self.playable = False
        self.basecard = True
        self.name = "Estate"
        self.cost = 2
        self.victory = 1

    @classmethod
    def calc_numcards(cls, game):
        if game.numplayers == 2:
            return 8 + game.numplayers * 3
        return 12 + game.numplayers * 3


# EOF
