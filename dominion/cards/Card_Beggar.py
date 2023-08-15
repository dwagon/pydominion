#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Beggar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Gain 3 Coppers, putting them into your hand.
            When another player plays an Attack card, you may discard this.
            If you do, gain two Silvers, putting one on top of your deck."""
        self.name = "Beggar"
        self.cost = 2

    def special(self, game, player):
        player.output("Gaining 3 coppers")
        for _ in range(3):
            player.gain_card("Copper", Piles.HAND)

    def hook_underAttack(self, game, player, attacker):
        player.output("Gaining silvers as under attack from %s" % attacker.name)
        player.gain_card("Silver", "topdeck")
        player.gain_card("Silver")


###############################################################################
class Test_Beggar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Beggar", "Militia"])
        self.g.start_game()
        self.plr, self.attacker = self.g.player_list()
        self.card = self.g["Beggar"].remove()

    def test_play(self):
        """Play a beggar"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])

    def test_attack(self):
        """React to an attack as a beggar"""
        self.plr.piles[Piles.HAND].set("Beggar", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        militia = self.g["Militia"].remove()
        self.attacker.add_card(militia, Piles.HAND)
        self.attacker.play_card(militia)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
