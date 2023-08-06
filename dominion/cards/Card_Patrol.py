#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Patrol(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+3 Cards; Reveal the top 4 cards of your deck.
            Put the Victory cards and Curses into your hand.
            Put the rest back in any order."""
        self.name = "Patrol"
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for _ in range(4):
            c = player.next_card()
            player.reveal_card(c)
            if c is None:
                break
            if c.isVictory() or c.name == "Curse":
                player.add_card(c, "hand")
                player.output(f"Patrol adding {c.name}")
            else:
                cards.add(c)
        for c in cards:
            player.output(f"Putting {c.name} back on deck")
            player.add_card(c, "topdeck")


###############################################################################
class Test_Patrol(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Patrol"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Patrol"].remove()

    def test_play(self):
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.deck.set("Duchy", "Province", "Silver", "Gold", "Copper", "Copper", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Province", self.plr.hand)
        self.assertIn("Duchy", self.plr.hand)
        self.assertNotIn("Silver", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
