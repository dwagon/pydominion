#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_IGG(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.HINTERLANDS
        self.required_cards = ["Curse"]
        self.name = "Ill-Gotten Gains"
        self.cost = 5
        self.coin = 1

    def desc(self, player):
        if player.phase == "buy":
            return """+1 Coin. When you play this, you may gain a Copper, putting
                it into your hand. When you gain this, each other player gains
                a Curse."""
        return "+1 Coin. When you play this, you may gain a Copper, putting it into your hand."

    def special(self, game, player):
        ans = player.plr_choose_options(
            "Gain a Copper into your hand?", ("No thanks", False), ("Gain Copper", True)
        )
        if ans:
            player.gain_card("Copper", destination="hand")

    def hook_gain_this_card(self, game, player):
        for plr in player.attack_victims():
            plr.gain_card("Curse")
            plr.output("Cursed because %s gained an Ill-Gotten Gains" % player.name)
        return {}


###############################################################################
class Test_IGG(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Ill-Gotten Gains"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Ill-Gotten Gains"].remove()

    def test_play(self):
        """Play an Ill-Gotten Gains"""
        self.plr.set_hand("Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["copper"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_hand("Copper"))
        self.assertEqual(self.plr.get_coins(), 1)

    def test_gain(self):
        """Gain an Ill-Gotten Gains"""
        self.plr.set_hand("Estate")
        self.plr.gain_card("Ill-Gotten Gains")
        self.assertIsNotNone(self.vic.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
