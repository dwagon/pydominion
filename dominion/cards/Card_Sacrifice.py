#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Sacrifice(Card.Card):
    """Sacrifice"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Trash a card from your hand. If it's an ...
            Action card: +2 Cards, +2 Actions; Treasure card: +2 Coin;
            Victory card: +2VP"""
        self.name = "Sacrifice"
        self.cost = 4

    def special(self, game, player):
        cards = player.plr_trash_card()
        if not cards:
            return
        card = cards[0]
        if card.isAction():
            player.pickup_cards(2)
            player.add_actions(2)
        if card.isTreasure():
            player.coins.add(2)
        if card.isVictory():
            player.add_score("Sacrifice", 2)


###############################################################################
class Test_Sacrifice(unittest.TestCase):
    """Test Sacrifice"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sacrifice", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sacrifice"].remove()

    def test_play_action(self):
        """Sacrifice an Action"""
        self.plr.hand.set("Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertIn("Moat", self.g.trashpile)

    def test_play_treasure(self):
        """Sacrifice a Treasure"""
        self.plr.hand.set("Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_play_victory(self):
        """Sacrifice a Victory"""
        self.plr.hand.set("Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Sacrifice"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
