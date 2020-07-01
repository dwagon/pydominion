#!/usr/bin/env python

import unittest
from cards.Card_Castles import CastleCard


###############################################################################
class Card_GrandCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = ['victory', 'castle']
        self.base = 'empires'
        self.cost = 9
        self.victory = 5
        self.name = "Grand Castle"

    def desc(self, player):
        if player.phase == "buy":
            return """5VP. When you gain this, reveal your hand. 1VP per Victory card in your hand and/or in play."""
        else:
            return "5VP"

    def hook_gainThisCard(self, game, player):
        for card in player.hand:
            player.revealCard(card)
        vics = sum([1 for _ in player.hand if _.isVictory()])
        player.output("Gaining %d VPs from your Victory Cards" % vics)
        player.addScore("Grand Castle", vics)
        for plr in list(game.players.values()):
            vics = sum([1 for card in plr.durationpile if card.isVictory()])
            player.output("Gaining %d VPs from %s's Victory Cards" % (vics, plr.name))
            player.addScore("Grand Castle", vics)


###############################################################################
class Test_GrandCastle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Castles'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        """ Play a sprawling castle"""
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Grand Castle':
                break
        self.plr.addCard(self.card, 'hand')
        self.assertEqual(self.plr.getScoreDetails()['Grand Castle'], 5)

    def test_gain(self):
        """ Gain Grand Castle """
        self.plr.setHand('Duchy', 'Province')
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Sprawling Castle':  # One before Grand
                break
        self.plr.gainCard('Castles')
        self.assertEqual(self.plr.getScoreDetails()['Grand Castle'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
