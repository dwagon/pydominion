#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Treasuremap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """Trash this and another copy of Treasure Map from your hand.
            If you do trash two Treasure Maps, gain 4 Gold cards, putting them
            on top of your deck."""
        self.name = "Treasure Map"
        self.cost = 4

    def special(self, game, player):
        player.trash_card(self)
        tmaps = [c for c in player.hand if c.name == "Treasure Map"][:1]
        if not tmaps:
            return
        t = player.plrTrashCard(
            prompt="If you trash another treasure map you can get 4 golds",
            cardsrc=tmaps,
        )
        if t:
            player.output("Gaining 4 Gold")
            for _ in range(4):
                player.gainCard("Gold", destination="topdeck")
        else:
            player.output("Didn't trash two so no Gold")


###############################################################################
class Test_Treasuremap(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Treasure Map"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Treasure Map"].remove()

    def test_trash(self):
        """Trash a TM"""
        tsize = self.g.trashSize()
        self.plr.set_deck()
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["0", "1", "finish"]
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Treasure Map"))
        self.assertEqual(self.plr.deck.size(), 0)

    def test_trash_two(self):
        """Trash 2 TM"""
        tsize = self.g.trashSize()
        self.plr.set_deck()
        self.plr.set_hand("Treasure Map")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["1", "finish"]
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertIsNotNone(self.g.in_trash("Treasure Map"))
        self.assertEqual(self.plr.deck.size(), 4)
        self.assertIsNotNone(self.plr.in_deck("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
