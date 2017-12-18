#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Moons_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocture'
        self.desc = "Look through your discard pile. You may put a card from it onto your deck"
        self.name = "The Moon's Gift"
        self.purchasable = False

    def special(self, game, player):
        if not player.discardSize():
            return
        cards = []
        cardnames = set()
        for c in player.discardpile:
            if c.name not in cardnames:
                cards.append(c)
                cardnames.add(c.name)
        card = player.cardSel(force=True, cardsrc=cards, prompt="Pull card from discard and add to top of your deck")
        player.addCard(card[0], 'topdeck')
        player.discardpile.remove(card[0])


###############################################################################
class Test_Moons_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons[:]:
            if b.name != "The Moon's Gift":
                self.g.discarded_boons.append(b)
                self.g.boons.remove(b)
        self.card = self.g['Bard'].remove()

    def test_moons_gift(self):
        self.plr.setDiscard('Province', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertIsNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
