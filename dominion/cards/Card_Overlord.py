#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Overlord """

import unittest
from dominion import Card, Game, Piles


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
class TestOverlord(unittest.TestCase):
    """Test Overlord"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Overlord", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Overlord")

    def test_play(self):
        """Play a Overlord"""
        hand = self.plr.piles[Piles.HAND].size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hand + 2)
        self.assertNotIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.g.card_piles["Moat"]), 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
