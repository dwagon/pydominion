#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Patron(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.RENAISSANCE
        self.desc = (
            "+1 Villager; +2. When something causes you to reveal this, +1 Coffers."
        )
        self.name = "Patron"
        self.cost = 4
        self.coin = 2

    def special(self, game, player):
        player.add_villager(1)

    def hook_revealThisCard(self, game, player):
        player.add_coffer()


###############################################################################
class Test_Patron(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Patron"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Patron"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_villagers(), 1)

    def test_reveal(self):
        num = self.plr.get_coffers()
        self.plr.reveal_card(self.card)
        self.assertEqual(self.plr.get_coffers(), num + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
