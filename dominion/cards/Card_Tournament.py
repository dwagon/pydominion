#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Tournament(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.CORNUCOPIA
        self.desc = """+1 Action. Each player may reveal a Province from his hand.
            If you do, discard it and gain a Prize (from the Prize pile) or a Duchy,
            putting it on top of your deck. If no-one else does, +1 Card, +1 Coin."""
        self.name = "Tournament"
        self.needsprize = True
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        found = False
        for plr in game.player_list():
            if plr != player:
                prov = plr.hand["Province"]
                if prov:
                    plr.reveal_card(prov)
                    found = True
        if "Province" in player.hand:
            player.output("Province revealed so gain a prize")
            player.discard_card(player.hand["Province"])
            player.gain_prize()
        if not found:
            player.output("No Province revealed")
            player.add_coins(1)
            player.pickup_card()


###############################################################################
class Test_Tournament(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Tournament"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Tournament"].remove()

    def test_play(self):
        """Play a tournament - no provinces"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_play_have_province(self):
        """Play a tournament - self provinces"""
        self.plr.test_input = ["Bag"]
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertIn("Bag of Gold", self.plr.discardpile)

    def test_play_all_province(self):
        """Play a tournament - others have provinces"""
        self.other.set_hand("Province")
        self.plr.test_input = ["Bag"]
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertIn("Bag of Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
