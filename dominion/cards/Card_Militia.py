#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
###############################################################################
class Card_Militia(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DOMINION
        self.desc = "+2 coin, Every other player discards down to 3"
        self.name = "Militia"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        """Every other player discards down to 3 cards"""
        for plr in player.attackVictims():
            plr.output("%s's Militia: Discard down to 3 cards" % player.name)
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Militia(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Militia", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.mcard = self.g["Militia"].remove()

    def test_defense(self):
        self.attacker.add_card(self.mcard, "hand")
        self.defender.add_card(self.g["Moat"].remove(), "hand")
        self.attacker.play_card(self.mcard)
        self.assertEqual(self.defender.hand.size(), 6)  # Normal + moat
        self.assertEqual(self.attacker.getCoin(), 2)

    def test_attack(self):
        self.attacker.add_card(self.mcard, "hand")
        self.defender.test_input = ["1", "2", "0"]
        self.attacker.play_card(self.mcard)
        self.assertEqual(self.defender.hand.size(), 3)  # Normal  - 2
        self.assertEqual(self.defender.discardpile.size(), 2)
        self.assertEqual(self.attacker.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
