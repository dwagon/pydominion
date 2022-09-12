#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Seer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """+1 Card; +1 Action; Reveal the top 3 cards of your deck.
            Put the ones costing from 2 to 4 into your hand. Put the rest back in any order."""
        self.cards = 1
        self.actions = 1
        self.name = "Seer"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        drawn = []
        for _ in range(3):
            c = player.next_card()
            player.reveal_card(c)
            if c.cost in (2, 3, 4) and not c.potcost and not c.debtcost:
                player.output(f"Putting {c} into your hand")
                player.add_card(c, "hand")
            else:
                drawn.append(c)
        for card in drawn:
            player.output(f"Putting {card} back on deck")
            player.add_card(card, "topdeck")


###############################################################################
class Test_Seer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Seer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Seer"].remove()

    def test_play(self):
        self.plr.deck.set("Copper", "Silver", "Estate", "Province")
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.plr.deck)
        self.assertIn("Province", self.plr.hand)
        self.assertIn("Silver", self.plr.hand)
        self.assertIn("Estate", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
