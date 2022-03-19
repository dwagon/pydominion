#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Hideout(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """+1 Card; +2 Actions; Trash a card from your hand. If it's a Victory card, gain a Curse."""
        self.name = "Hideout"
        self.required_cards = ["Curse"]
        self.actions = 2
        self.cards = 1
        self.cost = 4

    ###########################################################################
    def special(self, game, player):
        card = player.plr_trash_card(num=1, force=True)
        if card[0].isVictory():
            player.gain_card("Curse")


###############################################################################
class Test_Hideout(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hideout"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.plr.set_deck("Silver")
        self.plr.set_hand("Copper", "Estate")
        self.card = self.g["Hideout"].remove()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 2)

    def test_trashVictory(self):
        self.plr.set_deck("Silver")
        self.plr.set_hand("Copper", "Estate")
        self.card = self.g["Hideout"].remove()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertIsNotNone(self.plr.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
