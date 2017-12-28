#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Keep(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When scoring, 5VP per differently named Treasure you have, that you have more copies of than each other player, or tied for most."""
        self.name = "Keep"

    def hook_end_of_game(self, game, player):
        cards = {}
        # For each type of treasure card work out who has how many
        for pl in game.playerList():
            plname = pl.name
            for card in pl.allCards():
                if card.isTreasure():
                    if card.name not in cards:
                        cards[card.name] = {}
                    if plname not in cards[card.name]:
                        cards[card.name][plname] = 0
                    cards[card.name][plname] += 1

        # If player is the one who has the most, gain the points
        for card in cards:
            m = max(cards[card].values())
            if player.name in cards[card] and cards[card][player.name] == m:
                player.output("Gaining 5 from Landmark as you have the most %s (%d)" % (card, m))
                player.addScore('Keep', 5)


###############################################################################
class Test_Keep(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, landmarkcards=['Keep'], badcards=['Shepherd', 'Tracker', 'Fool', 'Cemetery', 'Pooka', 'Pixie'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()

    def test_most(self):
        """ Use Keep when we have the most Silver"""
        self.plr.setDeck('Silver')
        self.plr.gameOver()
        try:
            self.assertEqual(self.plr.getScoreDetails()['Keep'], 5)
        except AssertionError:
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
