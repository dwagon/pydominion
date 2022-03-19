#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Pooka(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.NOCTURNE
        self.desc = "You may trash a Treasure other than Cursed Gold from your hand, for +4 Cards."
        self.name = "Pooka"
        self.cost = 5
        self.heirloom = "Cursed Gold"

    def special(self, game, player):
        treasures = [
            _ for _ in player.hand if _.isTreasure() and _.name != "Cursed Gold"
        ]
        tr = player.plr_trash_card(
            prompt="Trash a treasure from your hand for +4 Cards", cardsrc=treasures
        )
        if tr:
            player.pickup_cards(4)


###############################################################################
class Test_Pooka(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pooka"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Pooka"].remove()

    def test_play(self):
        """Play a Pooka"""
        self.plr.set_hand("Copper", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIsNone(self.g.in_trash("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
