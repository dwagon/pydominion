#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Whens


###############################################################################
class Card_Ratcatcher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Card, +1 Action; Call to trash a card"
        self.name = "Ratcatcher"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.when = Whens.START

    def hook_call_reserve(self, game, player):
        """At the start of your turn, you may call this, to trash a
        card from your hand"""
        player.plr_trash_card()


###############################################################################
class Test_Ratcatcher(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Ratcatcher"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Ratcatcher")

    def test_play(self):
        """Play a ratcatcher"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertIn("Ratcatcher", self.plr.piles[Piles.RESERVE])

    def test_call(self):
        """Call from Reserve"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Gold"]
        self.plr.play_card(self.card)
        c = self.plr.call_reserve("Ratcatcher")
        self.assertEqual(c.name, "Ratcatcher")
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Gold", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
