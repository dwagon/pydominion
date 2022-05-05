#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Wanderingminstrel(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Card, +2 Actions. Reveal the top 3 cards of your deck.
            Put the Actions back on top in any order and discard the rest."""
        self.name = "Wandering Minstrel"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        cards = []
        for _ in range(3):
            c = player.next_card()
            player.reveal_card(c)
            if c.isAction():
                cards.append(c)
                player.output("Revealed a %s and put on top of deck" % c.name)
            else:
                player.add_card(c, "discard")
                player.output("Discarded %s" % c.name)

        for card in cards:
            player.add_card(card, "topdeck")


###############################################################################
class Test_Wanderingminstrel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wandering Minstrel", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Wandering Minstrel"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Wandering Minstrel"""
        self.plr.set_deck("Duchy", "Moat", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertIn("Moat", self.plr.deck)
        self.assertIn("Duchy", self.plr.discardpile)
        self.assertIn("Silver", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
