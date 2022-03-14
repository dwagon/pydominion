#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Margrave """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
###############################################################################
class Card_Margrave(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.HINTERLANDS
        self.desc = """+3 Card; +1 Buy; Each other player draws a card, then
            discards down to 3 cards in hand."""
        self.name = "Margrave"
        self.buys = 1
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """Each other player draws a card, then discards down to 3 cards in hand"""
        for plr in player.attack_victims():
            plr.pickup_card()
            plr.output("%s's Margrave: Discard down to 3 cards" % player.name)
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Margrave(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Margrave", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.card = self.g["Margrave"].remove()

    def test_defense(self):
        self.attacker.add_card(self.card, "hand")
        self.defender.add_card(self.g["Moat"].remove(), "hand")
        self.attacker.play_card(self.card)
        self.assertEqual(self.defender.hand.size(), 5 + 1)  # Moat
        self.assertEqual(self.attacker.hand.size(), 5 + 3)
        self.assertEqual(self.attacker.get_buys(), 1 + 1)

    def test_attack(self):
        self.attacker.add_card(self.card, "hand")
        self.defender.test_input = ["1", "2", "3", "0"]
        self.attacker.play_card(self.card)
        self.assertEqual(self.defender.hand.size(), 3)
        self.assertEqual(self.defender.discardpile.size(), 3)
        self.assertEqual(self.attacker.hand.size(), 5 + 3)
        self.assertEqual(self.attacker.get_buys(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
