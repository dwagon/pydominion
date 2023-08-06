#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Overlord """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Overlord(Card.Card):
    """Overlord"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.COMMAND]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "Play a non-Command Action card from the Supply costing up to $5, leaving it there."
        self.name = "Overlord"
        self.debtcost = 8

    def special(self, game, player):
        cards = [_ for _ in player.cards_under(5) if _.isAction() and not _.isCommand()]
        opts = [(f"Play {_.name}", _) for _ in cards]
        choice = player.plr_choose_options("Play which action card from supply?", *opts)
        player.play_card(choice, discard=False, cost_action=False)


###############################################################################
class Test_Overlord(unittest.TestCase):
    """Test Overlord"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Overlord", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Overlord"].remove()

    def test_play(self):
        """Play a Overlord"""
        hand = self.plr.hand.size()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Play Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hand + 2)
        self.assertNotIn("Moat", self.plr.played)
        self.assertEqual(len(self.g["Moat"]), 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
