#!/usr/bin/env python

import unittest
from dominion import Card, Game, State


###############################################################################
class State_Lost_in_woods(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.cardtype = Card.CardType.STATE
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "At the start of your turn, you may discard a card to receive a Boon."
        )
        self.name = "Lost in the Woods"
        self.unique_state = True

    def hook_start_turn(self, game, player):
        dc = player.plr_discard_cards(
            prompt="Lost in the Woods: Discard a card to receive a boon"
        )
        if dc:
            # Hack to make testing possible
            if not hasattr(player, "_liw_dont_boon"):
                player.receive_boon()
            else:
                player._liw_dont_boon = True


###############################################################################
class Test_Lost_in_woods(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.state = self.g.states["Lost in the Woods"]

    def test_lost_in_woods(self):
        self.plr.hand.set("Copper", "Estate", "Gold")
        self.plr.assign_state("Lost in the Woods")
        self.plr.test_input = ["Estate"]
        self.plr._liw_dont_boon = False
        self.plr.start_turn()
        self.assertTrue(self.plr._liw_dont_boon)
        self.assertIsNotNone(self.plr.discardpile["Estate"])

    def test_found_in_woods(self):
        self.plr.hand.set("Copper", "Estate", "Gold")
        self.plr.assign_state("Lost in the Woods")
        self.plr.test_input = ["Finish"]
        self.plr._liw_dont_boon = False
        self.plr.start_turn()
        self.assertFalse(self.plr._liw_dont_boon)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
