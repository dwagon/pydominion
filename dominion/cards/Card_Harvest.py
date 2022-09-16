#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Harvest(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """Reveal the top 4 cards of your deck, then discard them. Coin per differently named card revealed."""
        self.name = "Harvest"
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for _ in range(4):
            c = player.next_card()
            player.reveal_card(c)
            cards.add(c.name)
            player.output("Revealed a %s" % c.name)
            player.add_card(c, "discard")
        player.output("Gaining %d coins" % len(cards))
        player.coins.add(len(cards))


###############################################################################
class Test_Harvest(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Harvest"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Harvest"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Harvest"""
        self.plr.deck.set("Duchy", "Duchy", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertIn("Copper", self.plr.discardpile)
        self.assertNotIn("Duchy", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
