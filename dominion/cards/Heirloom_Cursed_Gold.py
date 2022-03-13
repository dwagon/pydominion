#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_CursedGold(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "3 Coin; When you play this, gain a curse"
        self.required_cards = ["Curse"]
        self.name = "Cursed Gold"
        self.cost = 4
        self.coin = 3
        self.purchasable = False

    def special(self, game, player):
        player.gainCard("Curse")


###############################################################################
class Test_CursedGold(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Pooka"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cursed Gold"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertEqual(self.plr.discardpile[0].name, "Curse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
