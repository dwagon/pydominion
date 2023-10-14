#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Architects%27_Guild"""

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Architects_Guild(Ally.Ally):
    """Architects Guild"""

    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = "When you gain a card, you may spend 2 Favors to gain a cheaper non-Victory card."
        self.name = "Architects' Guild"

    def hook_gain_card(self, game, player, card):
        if player.favors.get() < 2:
            return
        player.favors.add(-2)  # To stop re-triggering before favors are spent
        crd = player.plr_gain_card(
            cost=card.cost - 1,
            types={Card.CardType.ACTION: True, Card.CardType.TREASURE: True},
            prompt=f"Spend 2 favors to gain a card worth {card.cost-1} or less",
        )
        if not crd:
            player.favors.add(2)


###############################################################################
class Test_Architects_Guild(unittest.TestCase):
    """Test Architects Guild"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, allies="Architects Guild", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        """Play and gain a card"""
        self.plr.favors.set(2)
        self.plr.test_input = ["Get Silver"]
        self.plr.gain_card("Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.favors.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
