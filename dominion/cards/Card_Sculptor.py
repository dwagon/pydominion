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
            player.add_villager()


###############################################################################
class Test_Sculptor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sculptor", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sculptor"].remove()
        self.plr.set_hand()
        self.plr.add_card(self.card, "hand")

    def test_gainaction(self):
        self.plr.set_deck("Moat")
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 0)
        self.assertIsNotNone(self.plr.in_hand("Moat"))
        self.assertLessEqual(self.plr.get_villagers(), 1)

    def test_gaintreasure(self):
        self.plr.set_deck("Silver")
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_hand("Silver"))
        self.assertLessEqual(self.plr.get_villagers(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
