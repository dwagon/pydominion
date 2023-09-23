#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Witch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+2 cards; Each other player gains a Curse card."
        self.required_cards = ["Curse"]
        self.name = "Witch"
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """All other players gain a curse"""
        for pl in player.attack_victims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's witch cursed you" % player.name)
            pl.gain_card("Curse")


###############################################################################
class Test_Witch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Witch", "Moat"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.wcard = self.g.get_card_from_pile("Witch")
        self.mcard = self.g.get_card_from_pile("Moat")
        self.attacker.add_card(self.wcard, Piles.HAND)

    def test_defended(self):
        self.victim.add_card(self.mcard, Piles.HAND)
        self.attacker.play_card(self.wcard)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 0)

    def test_nodefense(self):
        self.attacker.play_card(self.wcard)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Curse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
