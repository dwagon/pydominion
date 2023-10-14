#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Charlatan"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Charlatan(Card.Card):
    """Charlatan"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+$3; Each other player gains a Curse."
        self.coin = 3
        self.name = "Charlatan"
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game, player):
        for victim in player.attack_victims():
            victim.output(f"{player.name}'s Charlatan curses you")
            victim.gain_card("Curse")


###############################################################################
class Test_Charlatan(unittest.TestCase):
    """Test Charlatan"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Charlatan"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Charlatan")

    def test_play_card(self):
        """Play a card"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_curse(self):
        """Test a curse"""
        curse = self.g.get_card_from_pile("Curse")
        self.plr.add_card(curse, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(curse)
        self.assertEqual(self.plr.coins.get(), coins + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
