#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Ninja"""
import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_Ninja(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.SHADOW]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "+1 Card; Each other player discards down to 3 cards in hand."
        self.name = "Ninja"
        self.cards = 1
        self.cost = 4

    def special(self, game, player):
        """Every other player discards down to 3 cards"""
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Ninja: Discard down to 3 cards")
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class TestNinja(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Ninja"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.card = self.g.get_card_from_pile("Ninja")

    def test_attack(self):
        self.attacker.add_card(self.card, Piles.HAND)
        self.defender.test_input = ["1", "2", "0"]
        hand_size = len(self.attacker.piles[Piles.HAND])
        self.attacker.play_card(self.card)
        self.assertEqual(self.defender.piles[Piles.HAND].size(), 3)  # Normal  - 2
        self.assertEqual(self.defender.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(len(self.attacker.piles[Piles.HAND]), hand_size + 1 - 1)  # -1 for playing


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
