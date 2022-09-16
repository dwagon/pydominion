#!/usr/bin/env python
"""  http://wiki.dominionstrategy.com/index.php/Plateau_Shepherds"""

import unittest
from dominion import Card, Game, Ally


###############################################################################
class Ally_Plateau_Shepherds(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When scoring, pair up your Favors with cards you have costing $2, for 2VP per pair. """
        self.name = "Plateau Shepherds"

    def special_score(self, game, player):
        twos = [_.name for _ in player.all_cards() if _.cost == 2]
        score = min(len(twos), player.favors.get()) * 2
        player.output(f"Gaining {score} from cards {', '.join(twos)})")
        return score


###############################################################################
class Test_Plateau_Shepherds(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Plateau Shepherds", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_score_less(self):
        """When we have less cards than favors"""
        self.plr.hand.set("Estate", "Estate")
        self.plr.deck.set("Silver", "Silver")
        self.plr.discardpile.set()
        self.plr.favors.set(4)
        score = self.plr.get_score_details()
        self.assertEqual(score["Plateau Shepherds"], 4)

    def test_score_more(self):
        """When we have more cards than favors"""
        self.plr.hand.set("Estate", "Estate", "Estate", "Estate")
        self.plr.deck.set("Silver", "Silver")
        self.plr.discardpile.set()
        self.plr.favors.set(3)
        score = self.plr.get_score_details()
        self.assertEqual(score["Plateau Shepherds"], 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
