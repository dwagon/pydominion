#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Caravan_Guard"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_CaravanGuard(Card.Card):
    """Caravan Guard"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Card, +1 Action. At the start of your next turn, +1 Coin.
            When another player plays an Attack card, you may play this from
            your hand. (+1 Action has no effect if it's not your turn.)"""
        self.name = "Caravan Guard"
        self.cost = 3

    def special(self, game, player):
        player.add_actions(1)
        player.pickup_cards(1)

    def duration(self, game, player):
        player.coins.add(1)

    def hook_underAttack(self, game, player, attacker):
        player.output(f"Under attack from {attacker.name}")
        player.pickup_cards(1)
        player.move_card(player.hand["Caravan Guard"], "played")


###############################################################################
class Test_CaravanGuard(unittest.TestCase):
    """Test Caravan Guard"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, initcards=["Caravan Guard", "Militia", "Moat"]
        )
        self.g.start_game()
        self.plr, self.attacker = self.g.player_list()
        self.card = self.g["Caravan Guard"].remove()
        self.militia = self.g["Militia"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Test playing the caravan guard"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)

    def test_attack(self):
        """Test being attacked"""
        self.plr.hand.set("Caravan Guard", "Moat")
        self.attacker.add_card(self.militia, "hand")
        self.attacker.play_card(self.militia)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertIn("Caravan Guard", self.plr.played)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
