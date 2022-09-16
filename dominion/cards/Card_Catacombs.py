#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Catacombs(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Look at the top 3 cards of your deck. Choose one: Put them
            into your hand; or discard them and +3 cards. When you trash this, gain a cheaper card."""
        self.name = "Catacombs"
        self.cost = 5

    def special(self, game, player):
        cards = []
        for _ in range(3):
            cards.append(player.next_card())
        player.output("You drew %s" % ", ".join([c.name for c in cards]))
        ans = player.plr_choose_options(
            "What do you want to do?",
            ("Keep the three", True),
            ("Discard and draw 3 more", False),
        )
        if ans:
            for c in cards:
                player.add_card(c, "hand")
        else:
            for c in cards:
                player.add_card(c, "discard")
            player.pickup_cards(3)

    def hook_trashThisCard(self, game, player):
        """When you trash this, gain a cheaper card"""
        player.plr_gain_card(cost=self.cost - 1)


###############################################################################
class Test_Catacombs(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Catacombs"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.cat = self.g["Catacombs"].remove()
        self.plr.add_card(self.cat, "hand")

    def test_keep(self):
        self.plr.deck.set("Province", "Gold", "Gold", "Gold")
        self.plr.test_input = ["keep the three"]
        self.plr.play_card(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(self.plr.hand.size(), 8)
        numgold = sum(1 for c in self.plr.hand if c.name == "Gold")
        self.assertEqual(numgold, 3)

    def test_discard(self):
        self.plr.deck.set("Province", "Province", "Province", "Gold", "Gold", "Gold")
        self.plr.test_input = ["discard and draw"]
        self.plr.play_card(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(self.plr.hand.size(), 8)
        numgold = sum(1 for c in self.plr.hand if c.name == "Gold")
        self.assertEqual(numgold, 0)
        numprov = sum(1 for c in self.plr.hand if c.name == "Province")
        self.assertEqual(numprov, 3)
        numgold = sum(1 for c in self.plr.discardpile if c.name == "Gold")
        self.assertEqual(numgold, 3)

    def test_trash(self):
        self.plr.test_input = ["get estate"]
        self.plr.trash_card(self.cat)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertTrue(self.plr.discardpile[0].cost < self.cat.cost)
        self.assertIn("Catacombs", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
