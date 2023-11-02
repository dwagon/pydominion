#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Margrave """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Margrave(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+3 Card; +1 Buy; Each other player draws a card, then
            discards down to 3 cards in hand."""
        self.name = "Margrave"
        self.buys = 1
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """Each other player draws a card, then discards down to 3 cards in hand"""
        for plr in player.attack_victims():
            plr.pickup_cards(1)
            plr.output(f"{player.name}'s Margrave: Discard down to 3 cards")
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class TestMargrave(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Margrave", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.card = self.g.get_card_from_pile("Margrave")

    def test_defense(self):
        self.attacker.add_card(self.card, Piles.HAND)
        self.defender.add_card(self.g.get_card_from_pile("Moat"), Piles.HAND)
        self.attacker.play_card(self.card)
        self.assertEqual(self.defender.piles[Piles.HAND].size(), 5 + 1)  # Moat
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 3)
        self.assertEqual(self.attacker.buys.get(), 1 + 1)

    def test_attack(self):
        self.attacker.add_card(self.card, Piles.HAND)
        self.defender.test_input = ["1", "2", "3", "0"]
        self.attacker.play_card(self.card)
        self.assertEqual(self.defender.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.defender.piles[Piles.DISCARD].size(), 3)
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 3)
        self.assertEqual(self.attacker.buys.get(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
