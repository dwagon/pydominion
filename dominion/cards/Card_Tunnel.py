#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Tunnel(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_REACTION]
        self.base = Game.HINTERLANDS
        self.desc = """2VP. When you discard this other than during a Clean-up phase, you may reveal it. If you do, gain a Gold."""
        self.name = "Tunnel"
        self.cost = 3
        self.victory = 2

    def hook_discard_this_card(self, game, player, source):
        if player.phase == "cleanup":
            return
        gain = player.plrChooseOptions(
            "Gain a Gold from your Tunnel?", ("No thanks", False), ("Gain Gold?", True)
        )
        if gain:
            player.gainCard("Gold")


###############################################################################
class Test_Tunnel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Tunnel"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Tunnel"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the Tunnel"""
        self.plr.test_input = ["gold"]
        self.plr.discard_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))

    def test_score(self):
        """Score from a Tunnel"""
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Tunnel"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
