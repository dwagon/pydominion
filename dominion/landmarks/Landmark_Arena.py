#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Arena"""
import unittest

from dominion import Card, Game, Piles, Landmark, Player

ARENA = "arena"


###############################################################################
class Landmark_Arena(Landmark.Landmark):
    """Arena"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Arena"

    def dynamic_description(self, player: "Player.Player") -> str:
        return f"""At the start of your Buy phase, you may discard an Action card.
                If you do, take 2VP from here. ({player.game.specials[ARENA]} left)"""

    def setup(self, game: "Game.Game") -> None:
        game.specials[ARENA] = 6 * game.numplayers

    def hook_pre_buy(self, game: "Game.Game", player: "Player.Player") -> None:
        if game.specials[ARENA] <= 0:
            return
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            return
        if player.plr_discard_cards(prompt="Arena: Discard an action to gain 2VP", cardsrc=actions):
            player.output("Gained 2 VP from Arena")
            game.specials[ARENA] -= 2
            player.add_score("Arena", 2)


###############################################################################
class Test_Arena(unittest.TestCase):
    """Test Arena"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Arena"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Arena"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Discard Moat", "End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.get_score_details()["Arena"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
