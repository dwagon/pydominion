#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Forager(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Action +1 Buy;Trash a card from your hand. A coin per differently named Treasure in the trash."""
        self.name = "Forager"
        self.actions = 1
        self.buys = 1
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        player.plrTrashCard()
        treas = set()
        for card in game.trashpile:
            if card.isTreasure():
                treas.add(card.name)
        player.addCoin(len(treas))
        player.output("Gained %s from Forager" % len(treas))


###############################################################################
class Test_Forager(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Forager"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Forager"].remove()

    def test_play(self):
        """Play a forager"""
        self.plr.trash_card(self.g["Copper"].remove())
        self.plr.trash_card(self.g["Silver"].remove())
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertEqual(self.plr.get_coins(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
