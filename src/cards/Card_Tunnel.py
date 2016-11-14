#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Tunnel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['victory', 'reaction']
        self.base = 'hinterland'
        self.desc = """2VP. When you discard this other than during a Clean-up phase, you may reveal it. If you do, gain a Gold."""
        self.name = "Tunnel"
        self.cost = 3
        self.victory = 2

    def hook_discardThisCard(self, game, player):
        if player.phase == 'cleanup':
            return
        gain = player.plrChooseOptions(
            "Gain a Gold from your Tunnel?",
            ("No thanks", False),
            ("Gain Gold?", True))
        if gain:
            player.gainCard('Gold')


###############################################################################
class Test_Tunnel(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Tunnel"])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g["Tunnel"].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the Tunnel """
        self.plr.test_input = ['gold']
        self.plr.discardCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))

    def test_score(self):
        """ Score from a Tunnel """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Tunnel'], 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
