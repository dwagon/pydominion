#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_WilloWisp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SPIRIT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card; +1 Action; Reveal the top card of your deck. If it costs 2 or less, put it into your hand."
        self.name = "Will-o'-Wisp"
        self.purchasable = False
        self.cards = 1
        self.actions = 1
        self.insupply = False
        self.cost = 0

    def special(self, game, player):
        c = player.next_card()
        player.reveal_card(c)
        if c.cost <= 2 and not c.potcost and not c.debtcost:
            player.add_card(c, Piles.HAND)
            player.output(f"Moving {c.name} from your deck to your hand")
        else:
            player.add_card(c, "topdeck")
            player.output(f"Keep {c.name} on top of your deck")


###############################################################################
class Test_WilloWisp(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Will-o'-Wisp"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Will-o'-Wisp"].remove()

    def test_special_cheap(self):
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])

    def test_special_expensive(self):
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
