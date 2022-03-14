#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Mercenary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DARKAGES
        self.desc = """You may trash 2 cards from your hand.
        If you do, +2 Cards, +2 Coin, and each other player discards down to 3 cards in hand."""
        self.name = "Mercenary"
        self.insupply = False
        self.purchasable = False
        self.cost = 0

    def special(self, game, player):
        """You may trash 2 cards from your hand. If you do, +2
        cards, +2 coin, and each other player discards down to 3
        cards in hand"""

        ans = player.plrChooseOptions(
            "Trash cards?", ("Trash nothing", False), ("Trash 2 cards", True)
        )
        if not ans:
            return
        player.plrTrashCard(2, force=True)
        player.pickup_cards(2)
        player.addCoin(2)
        for plr in player.attackVictims():
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Mercenary(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Urchin", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Mercenary"].remove()

    def test_play(self):
        """Trash nothing with mercenary - should do nothing"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertTrue(self.victim.discardpile.is_empty())

    def test_defense(self):
        """Make sure moats work against mercenaries"""
        tsize = self.g.trashSize()
        self.plr.add_card(self.card, "hand")
        moat = self.g["Moat"].remove()
        self.victim.add_card(moat, "hand")
        self.plr.test_input = ["1", "1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertEqual(self.plr.hand.size(), 5)
        # 5 for hand + moat
        self.assertEqual(self.victim.hand.size(), 6)
        self.assertTrue(self.victim.discardpile.is_empty())

    def test_attack(self):
        """Attack with a mercenary"""
        tsize = self.g.trashSize()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1", "1", "2", "0"]
        self.victim.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.victim.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
