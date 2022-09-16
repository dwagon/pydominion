#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Forge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "Trash cards from hand and gain one worth the sum of the trashed cards"
        self.name = "Forge"
        self.cost = 7

    ###########################################################################
    def special(self, game, player):
        """Trash any number of cards from your hand. Gain a card
        with cost exactly equal to the total cost in coins of the
        trashed cards."""
        availcosts = set()
        for cp in game.cardTypes():
            availcosts.add(f"{cp.cost}")
        player.output("Gain a card costing exactly the sum of the trashed cards")
        player.output("Costs = %s" % ", ".join(sorted(list(availcosts))))
        tc = player.plr_trash_card(anynum=True, num=0, printcost=True)
        cost = sum(_.cost for _ in tc)
        player.plr_gain_card(cost=cost, modifier="equal", prompt=f"Gain card worth {cost}")


###############################################################################
class Test_Forge(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forge", "Bureaucrat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.forge = self.g["Forge"].remove()

    def test_play(self):
        """Play the Forge"""
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Estate", "Estate", "Estate")
        self.plr.add_card(self.forge, "hand")
        # Trash two cards, Finish Trashing, Select another
        self.plr.test_input = ["1", "2", "finish", "Bureaucrat"]
        self.plr.play_card(self.forge)
        self.assertEqual(self.plr.discardpile[0].cost, 4)
        self.assertIn("Estate", self.g.trashpile)
        self.assertEqual(self.g.trashpile.size(), tsize + 2)
        self.assertEqual(self.plr.hand.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
