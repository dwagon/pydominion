#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_MountainPass(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Mountain Pass"
        self._state = "un"

    def desc(self, player):
        if self._state == "done":
            return "Mountain Pass already claimed"
        return """When you are the first player to gain a Province, after that turn,
            each player bids once, up to 40 Debt, ending with you.
            High bidder gets +8VP and takes the Debt they bid."""

    def hook_end_turn(self, game, player):
        if self._state == "do":
            plr = player
            curbid = 0
            winning_plr = None
            while True:
                plr = game.playerToRight(plr)
                opts = self.generate_bids(curbid)
                bid = plr.plrChooseOptions("What to bid for 8VP?", *opts)
                if bid > curbid:
                    curbid = bid
                    winning_plr = plr
                if plr == player:
                    break

            if winning_plr:
                winning_plr.debt += curbid
                winning_plr.addScore('Mountain Pass', 8)
                game.output("%s won with a bid of %d for 8VP" % (winning_plr.name, curbid))
                self._state = "done"
            else:
                game.output("No one bid for Mountain Pass")

    def hook_gain_card(self, game, player, card):
        if self._state != "un":
            return
        if card.name == "Province":
            self._state = "do"

    def generate_bids(self, minbid):
        options = []
        options.append(("Don't bid", -1))
        for i in range(minbid+1, 41):
            options.append(("Bid %d" % i, i))
        return options


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return 0


###############################################################################
class Test_MountainPass(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, landmarkcards=['Mountain Pass'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.mp = self.g.landmarks['Mountain Pass']

    def test_play(self):
        """ Test Mountain Pass"""
        self.assertEqual(self.mp._state, 'un')
        self.plr.gainCard('Province')
        self.assertEqual(self.mp._state, 'do')
        self.other.test_input = ['24']
        self.plr.test_input = ['25']
        self.plr.end_turn()
        self.assertEqual(self.plr.debt, 25)
        self.assertEqual(self.other.debt, 0)
        self.assertEqual(self.plr.getScoreDetails()['Mountain Pass'], 8)
        self.assertNotIn('Mountain Pass', self.other.getScoreDetails())
        self.assertEqual(self.mp._state, 'done')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
