#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_BagOfGold(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.PRIZE]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.name = "Bag of Gold"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action. Gain a Gold, putting it on top of your deck."
        self.actions = 1

    def special(self, game, player):
        player.gain_card("Gold", "topdeck")


###############################################################################
class TestBagOfGold(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Bag of Gold"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
