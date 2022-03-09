#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Outpost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.SEASIDE
        self.desc = """You only draw 3 cards (instead of 5) in this turn's Clean-up phase.
        Take an extra turn after this one.
        This can't cause you to take more than two consecutive turns."""
        self.name = "Outpost"
        self.cost = 5

    def hook_cleanup(self, game, player):
        player.newhandsize = 3

    def hook_end_turn(self, game, player):
        if player.newhandsize == 3:
            player.output("Having a second turn due to Output")
            game.current_player = game.playerToRight(player)
        else:
            player.output("Already had one extra turn")


###############################################################################
class Test_Outpost(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Outpost"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Outpost"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play Outpost"""
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.g.print_state()
        # TODO - Not sure how to test this


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
