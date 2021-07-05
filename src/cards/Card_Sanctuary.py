#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sanctuary """

import unittest
import Game
import Card


###############################################################################
class Card_Sanctuary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = (
            """+1 Card; +1 Action; +1 Buy; You may Exile a card from your hand."""
        )
        self.name = "Sanctuary"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.buys = 1

    def special(self, game, player):
        crd = player.cardSel(prompt="Exile a card", verbs=("Exile", "Unexile"))
        if crd:
            player.hand.remove(crd[0])
            player.exile_card(crd[0])


###############################################################################
class Test_Sanctuary(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Sanctuary"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sanctuary"].remove()

    def test_playcard(self):
        """Play a card"""
        self.plr.setDeck("Estate", "Duchy", "Province")
        self.plr.setHand("Copper", "Silver", "Gold")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Exile Copper"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNotNone(self.plr.in_exile("Copper"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
