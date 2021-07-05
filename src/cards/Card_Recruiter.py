#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Recruiter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = (
            """+2 Cards; Trash a card from your hand. +1 Villager per coin it costs."""
        )
        self.name = "Recruiter"
        self.cards = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        cards = player.plrTrashCard(force=True, num=1)
        player.gainVillager(cards[0].cost)


###############################################################################
class Test_Recruiter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Recruiter"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Recruiter"].remove()

    def test_play(self):
        self.plr.setHand("Copper", "Silver")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Trash Silver"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 2 + 1)
        self.assertEqual(self.plr.getVillager(), 3)
        self.assertIsNotNone(self.g.in_trash("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
