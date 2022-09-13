#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Sculptor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """Gain a card to your hand costing up to 4. If it's a Treasure, +1 Villager."""
        self.name = "Sculptor"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        card = player.plr_gain_card(4, destination="hand", force=True)
        if card.isTreasure():
            player.output("Gained  villager")
            player.villagers.add(1)


###############################################################################
class Test_Sculptor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sculptor", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sculptor"].remove()
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")

    def test_gainaction(self):
        self.plr.deck.set("Moat")
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 0)
        self.assertIn("Moat", self.plr.hand)
        self.assertLessEqual(self.plr.villagers.get(), 1)

    def test_gaintreasure(self):
        self.plr.deck.set("Silver")
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.hand)
        self.assertLessEqual(self.plr.villagers.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
