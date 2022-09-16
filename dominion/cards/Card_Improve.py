#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Improve(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+2 Coin; At the start of Clean-up, you may trash an Action
        card you would discard from play this turn, to gain a card costing exactly
        1 more than it."""
        self.name = "Improve"
        self.cost = 3
        self.coin = 2

    def hook_cleanup(self, game, player):
        acts = [_ for _ in player.hand + player.discardpile if _.isAction()]
        if not acts:
            return
        tt = player.plr_trash_card(cardsrc=acts, prompt="Trash a card through Improve")
        if not tt:
            return
        cost = tt[0].cost
        player.plr_gain_card(cost + 1, modifier="equal")


###############################################################################
class Test_Improve(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Improve", "Moat", "Guide"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Improve"].remove()
        self.card.player = self.plr

    def test_play(self):
        self.plr.hand.set("Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.plr.test_input = ["End phase", "End phase", "Trash Moat", "Get Guide"]
        self.plr.turn()
        self.assertIn("Moat", self.g.trashpile)
        self.assertIn("Guide", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
