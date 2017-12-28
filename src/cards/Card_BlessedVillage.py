#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_BlessedVillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.base = 'nocturne'
        self.name = 'Blessed Village'
        self.actions = 2
        self.cards = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            self.desc = "+1 Card; +2 Actions; When you gain this, take a Boon. Receive it now or at the start of your next turn."
        else:
            self.desc = "+1 Card; +2 Actions"

    def hook_gainThisCard(self, game, player):
        player.receive_boon()


###############################################################################
class Test_BlessedVillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Blessed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Blessed Village'].remove()
        for b in self.g.boons:
            if b.name == "The Sea's Gift":
                myboon = b
                break
        self.g.boons = [myboon]

    def test_play_card(self):
        """ Play Blessed Village """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertGreaterEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 6)

    def test_gain(self):
        self.plr.gainCard('Blessed Village')
        self.assertEqual(self.plr.handSize(), 5 + 1)    # 1 from boon


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
