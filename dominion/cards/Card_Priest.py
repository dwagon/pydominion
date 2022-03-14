#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Priest(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.name = "Priest"
        self.desc = "+2 Coin. Trash a card from your hand. For the rest of this turn, when you trash a card, +2 Coin."
        self.cost = 4
        self.coin = 2
        self.in_special = False

    ###########################################################################
    def special(self, game, player):
        self.in_special = True
        player.plrTrashCard(force=True)
        self.in_special = False

    ###########################################################################
    def hook_trash_card(self, game, player, card):
        if not self.in_special:
            player.output("Adding 2 from Priest")
            player.addCoin(2)


###############################################################################
class Test_Priest(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Priest", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Priest"].remove()
        self.plr.add_card(self.card, "hand")
        self.moat = self.g["Moat"].remove()
        self.plr.add_card(self.moat, "hand")
        self.gold = self.g["Gold"].remove()
        self.plr.add_card(self.gold, "hand")

    def test_play_card(self):
        self.plr.test_input = ["Trash Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIsNotNone(self.g.in_trash("Moat"))
        self.plr.trash_card(self.gold)
        self.assertEqual(self.plr.get_coins(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
