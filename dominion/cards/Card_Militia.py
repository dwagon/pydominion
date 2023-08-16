#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
###############################################################################
class Card_Militia(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+2 coin, Every other player discards down to 3"
        self.name = "Militia"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        """Every other player discards down to 3 cards"""
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Militia: Discard down to 3 cards")
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class TestMilitia(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Militia", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.mcard = self.g["Militia"].remove()

    def test_defense(self):
        self.attacker.add_card(self.mcard, Piles.HAND)
        self.defender.add_card(self.g["Moat"].remove(), Piles.HAND)
        self.attacker.play_card(self.mcard)
        self.assertEqual(self.defender.piles[Piles.HAND].size(), 6)  # Normal + moat
        self.assertEqual(self.attacker.coins.get(), 2)

    def test_attack(self):
        self.attacker.add_card(self.mcard, Piles.HAND)
        self.defender.test_input = ["1", "2", "0"]
        self.attacker.play_card(self.mcard)
        self.assertEqual(self.defender.piles[Piles.HAND].size(), 3)  # Normal  - 2
        self.assertEqual(self.defender.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.attacker.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
