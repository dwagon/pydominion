#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Venture(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.desc = "+1 coin, get next treasure from deck"
        self.base = Game.PROSPERITY
        self.name = "Venture"
        self.cost = 5

    def special(self, game, player):
        """When you play this, reveal cards from your deck until
        you reveal a Treasure. Discard the other cards. Play that
        Treasure"""
        while True:
            c = player.pickup_card(verbose=False)
            player.reveal_card(c)
            if c.isTreasure():
                player.output("Picked up %s from Venture" % c.name)
                player.play_card(c)
                break
            player.output("Picked up and discarded %s" % c.name)
            player.add_coins(c.coin)  # Compensate for not keeping card
            player.discard_card(c)


###############################################################################
class Test_Venture(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Venture"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Venture"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Venture"""
        self.plr.deck.set("Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)  # Gold
        for c in self.plr.played:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertTrue(self.plr.deck.is_empty())

    def test_discard(self):
        """Make sure we discard non-treasures"""
        self.plr.deck.set("Gold", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)  # Gold
        for c in self.plr.played:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            if c.name != "Estate":  # pragma: no cover
                self.fail("Didn't discard the non-treasure")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
