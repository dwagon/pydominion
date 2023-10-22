#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Forge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = (
            "Trash cards from hand and gain one worth the sum of the trashed cards"
        )
        self.name = "Forge"
        self.cost = 7

    ###########################################################################
    def special(self, game, player):
        """Trash any number of cards from your hand. Gain a card
        with cost exactly equal to the total cost in coins of the
        trashed cards."""
        player.output("Gain a card costing exactly the sum of the trashed cards")
        tc = player.plr_trash_card(anynum=True, num=0, printcost=True)
        cost = sum(_.cost for _ in tc)
        player.plr_gain_card(
            cost=cost, modifier="equal", prompt=f"Gain card worth {cost}"
        )


###############################################################################
class TestForge(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forge", "Bureaucrat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.forge = self.g.get_card_from_pile("Forge")

    def test_play(self):
        """Play the Forge"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate")
        self.plr.add_card(self.forge, Piles.HAND)
        # Trash two cards, Finish Trashing, Select another
        self.plr.test_input = ["1", "2", "finish", "Bureaucrat"]
        self.plr.play_card(self.forge)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].cost, 4)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
