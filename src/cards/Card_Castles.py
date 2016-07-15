#!/usr/bin/env python

from Card import Card
from CardPile import CardPile
import unittest


###############################################################################
class Card_Castles(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = 'Castles'

    def setup(self, game):
        game.cardpiles['Castles'] = CastleCardPile(game.cardmapping['Castle'])


###############################################################################
class CastleCardPile(CardPile):
    def __init__(self, mapping, numcards=10):
        self.numcards = numcards
        self.embargo_level = 0
        castletypes = mapping

        self.castles = sorted([c() for c in castletypes.values()], key=lambda x: x.cost, reverse=True)

    def __getattr__(self, key):
        try:
            if key == 'card':
                return self.castles[-1]
            return getattr(self.castles[-1], key)
        except IndexError:
            return None

    def remove(self):
        if self.castles:
            self.numcards -= 1
            return self.castles.pop()
        else:
            return None

    def __repr__(self):
        return "CastleCardPile %s: %d" % (self.name, self.numcards)


###############################################################################
class CastleCard(Card):
    pass


###############################################################################
class Test_Castle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Castles'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Castles'].remove()
        self.plr.setHand('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')

    def test_castles(self):
        pass

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
