#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, State, Player

LOST_IN_WOODS = "Lost in the Woods"


###############################################################################
class State_Lost_in_woods(State.State):
    def __init__(self) -> None:
        State.State.__init__(self)
        self.cardtype = Card.CardType.STATE
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "At the start of your turn, you may discard a card to receive a Boon."
        )
        self.name = "Lost in the Woods"
        self.unique_state = True

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.plr_discard_cards(
            prompt="Lost in the Woods: Discard a card to receive a boon"
        ):
            player.specials[LOST_IN_WOODS] = True  # For testing
            player.receive_boon()


###############################################################################
class TestLostInWoods(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.state = self.g.states["Lost in the Woods"]

    def test_discard(self) -> None:
        """Lost in the Woods and discard"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.assign_state("Lost in the Woods")
        # Finish is for the gained boon
        self.plr.test_input = ["Discard Estate", "Finish"]
        self.plr.specials[LOST_IN_WOODS] = False
        self.plr.start_turn()
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.plr.specials[LOST_IN_WOODS])

    def test_dont_discard(self) -> None:
        """Lost in the Woods and don't discard"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Gold")
        self.plr.assign_state("Lost in the Woods")
        self.plr.specials[LOST_IN_WOODS] = False
        self.plr.test_input = ["Finish"]
        self.plr.start_turn()
        self.assertNotIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertFalse(self.plr.specials[LOST_IN_WOODS])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
