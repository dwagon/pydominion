#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Guard_Dog """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Guard_Dog(Card.Card):
    """Guard Dog"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+2 Cards; If you have 5 or fewer cards in hand, +2 Cards.
            When another player plays an Attack, you may first play this from your hand."""
        self.name = "Guard Dog"
        self.cost = 3

    def special(self, game, player):
        player.pickup_cards(2)
        if player.piles[Piles.HAND].size() <= 5:
            player.pickup_cards(2)

    def hook_underAttack(self, game, player, attacker):
        player.output(f"Playing Guard Dog as under attack by {attacker.name}")
        player.play_card(self, cost_action=False)


###############################################################################
class TestGuardDog(unittest.TestCase):
    """Test Guard Dog"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Guard Dog", "Witch"])
        self.g.start_game()
        self.plr, self.att = self.g.player_list()
        self.card = self.g["Guard Dog"].remove()

    def test_play_small_hand(self):
        """Play a card - gain twice"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_play_big_hand(self):
        """Play a card - gain once"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_attack(self):
        """Test under attack"""
        self.plr.piles[Piles.HAND].set("Copper", "Guard Dog")
        witch = self.g.get_card_from_pile("Witch")
        self.att.add_card(witch, Piles.HAND)
        self.att.play_card(witch)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertIn("Guard Dog", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
