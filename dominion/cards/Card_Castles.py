#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card
import dominion.CardPile as CardPile


###############################################################################
class Card_Castles(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Castles"
        self.base = Game.EMPIRES

    def setup(self, game):
        game.cardpiles["Castles"] = CastleCardPile(game.cardmapping["Castle"])


###############################################################################
class CastleCardPile(CardPile.CardPile):
    def __init__(self, mapping, numcards=10):
        self.pilesize = numcards
        self.embargo_level = 0
        castletypes = mapping

        self.castles = sorted(
            [c() for c in castletypes.values()], key=lambda x: x.cost, reverse=True
        )

    def __getattr__(self, key):
        try:
            if key == "card":
                return self.castles[-1]
            return getattr(self.castles[-1], key)
        except IndexError:
            return None

    def remove(self):
        if self.castles:
            self.pilesize -= 1
            return self.castles.pop()
        return None

    def __repr__(self):
        return "CastleCardPile %s: %d" % (self.name, self.pilesize)


###############################################################################
class CastleCard(Card.Card):
    pass


###############################################################################
class Test_Castle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Castles"].remove()
        self.plr.set_hand("Silver", "Gold")
        self.plr.addCard(self.card, "hand")

    def test_castles(self):
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
