#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Baths"""
import unittest

from dominion import Card, Game, Landmark

BATHS = "baths"


###############################################################################
class Landmark_Baths(Landmark.Landmark):
    """Baths"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Baths"

    def dynamic_description(self, player):
        return f"""When you end your turn without having gained a card,
            take 2VP from here. ({player.game.specials[BATHS]} left)"""

    def hook_end_turn(self, game, player):
        if not player.stats["gained"]:
            player.output("Gaining 2 from Baths as no cards gained")
            player.add_score("Baths", 2)
            game.specials[BATHS] -= 2

    def setup(self, game):
        game.specials[BATHS] = 6 * game.numplayers


###############################################################################
class Test_Baths(unittest.TestCase):
    """Test Baths"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Baths"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_use(self):
        """Use Baths"""
        self.plr.coin = 4
        self.plr.end_turn()
        self.assertEqual(self.plr.get_score_details()["Baths"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
