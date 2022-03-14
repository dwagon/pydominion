#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_CursedVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DOOM]
        self.base = Game.NOCTURNE
        self.desc = "+2 Actions. Draw until you have 6 cards in hand. When you gain this, receive a Hex."
        self.name = "Cursed Village"
        self.actions = 2
        self.cost = 5

    def special(self, game, player):
        while player.hand.size() < 6:
            c = player.next_card()
            player.add_card(c, "discard")
            player.pickup_card(c)

    def hook_gain_this_card(self, game, player):
        player.receive_hex()


###############################################################################
class Test_CursedVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cursed Village"].remove()
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_card(self):
        """Play Cursed Village"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_gain(self):
        self.plr.gainCard("Cursed Village")
        self.assertTrue(self.plr.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
