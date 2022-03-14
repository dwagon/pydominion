#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Groom """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Groom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.cost = 4
        self.name = "Groom"
        self.base = Game.MENAGERIE
        self.desc = """Gain a card costing up to 4 Coin. If it's an...
            Action card, gain a Horse;
            Treasure card, gain a Silver;
            Victory card, +1 Card and +1 Action."""
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        card = player.plrGainCard(4)
        if card.isAction():
            player.gain_card("Horse")
        if card.isTreasure():
            player.gain_card("Silver")
        if card.isVictory():
            player.pickup_card()
            player.addActions(1)


###############################################################################
class Test_Groom(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Groom", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Groom"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard_action(self):
        """Play Card"""
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Horse"))

    def test_playcard_victory(self):
        """Play Card"""
        self.plr.test_input = ["Get Estate"]
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_discard("Horse"))
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
