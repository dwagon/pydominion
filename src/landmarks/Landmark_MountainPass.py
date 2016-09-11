#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_MountainPass(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.name = "Mountain Pass"
        self.desc = """When you are the first player to gain a Province, after that turn,
            each player bids once, up to 40 Debt, ending with you.
            High bidder gets +8VP and takes the Debt they bid."""
        self._state = "un"

    def hook_endTurn(self, game, player):
        if self._state == "do":
            plr = player
            curbid = 1
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

            winning_plr.debt += curbid
            winning_plr.addScore('Mountain Pass', 8)
            game.output("%s bid %d for 8VP" % (winning_plr.name, curbid))
            self._state = "done"

    def hook_gainCard(self, game, player, card):
        if self._state != "un":
            return
        # if card.name == "Province":
        if card.name == "Copper":
            self._state = "do"

    def generate_bids(self, minbid):
        options = []
        options.append(("Don't bid", 0))
        for i in range(minbid, 41):
            options.append(("Bid %d" % i, i))
        return options


###############################################################################
class Test_MountainPass(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Mountain Pass'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_play(self):
        """ Test Mountain Pass"""
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
