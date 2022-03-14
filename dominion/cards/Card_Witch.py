#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Witch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DOMINION
        self.desc = "+2 cards; Each other player gains a Curse card."
        self.required_cards = ["Curse"]
        self.name = "Witch"
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """All other players gain a curse"""
        for pl in player.attackVictims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's witch cursed you" % player.name)
            pl.gainCard("Curse")


###############################################################################
class Test_Witch(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Witch", "Moat"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.wcard = self.g["Witch"].remove()
        self.mcard = self.g["Moat"].remove()
        self.attacker.add_card(self.wcard, "hand")

    def test_defended(self):
        self.victim.add_card(self.mcard, "hand")
        self.attacker.play_card(self.wcard)
        self.assertEqual(self.victim.hand.size(), 6)
        self.assertEqual(self.attacker.hand.size(), 7)
        self.assertEqual(self.victim.discardpile.size(), 0)

    def test_nodefense(self):
        self.attacker.play_card(self.wcard)
        self.assertEqual(self.victim.hand.size(), 5)
        self.assertEqual(self.attacker.hand.size(), 7)
        self.assertEqual(self.victim.discardpile[0].name, "Curse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
