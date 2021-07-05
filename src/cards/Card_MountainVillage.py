#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_MountainVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = "+2 Actions; Look through your discard pile and put a card from it into your hand; if you can't, +1 Card."
        self.name = "Mountain Village"
        self.cost = 4
        self.actions = 2

    def special(self, game, player):
        if player.discardpile.size():
            card = player.cardSel(
                cardsrc="discard",
                force=True,
                prompt="Look through your discard pile and put a card from it into your hand",
            )
            player.discardpile.remove(card[0])
            player.addCard(card[0], "hand")
        else:
            player.output("No cards in discard pile")
            player.pickupCards(1)


###############################################################################
class Test_MountainVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Mountain Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mountain Village"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play_no_discard(self):
        """Play Mountain Village without a discard card"""
        self.plr.setDiscard()
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_play_discard(self):
        """Play Mountain Village with a discard card"""
        self.plr.setDiscard("Gold", "Silver")
        self.plr.test_input = ["Gold"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertIsNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
