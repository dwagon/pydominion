#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Kingscourt(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Play action 3 times"
        self.name = "King's Court"
        self.cost = 7

    def special(self, game, player):
        """ You may chose an Action card in your hand. Play it three times """
        options = [{'selector': '0', 'print': "Don't play a card", 'card': None}]
        index = 1
        for c in player.hand:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s thrice" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        if index == 1:
            player.output("No action cards to repeat")
            return
        o = player.userInput(options, "Play which action card three times?")
        if not o['card']:
            return
        for i in range(1, 4):
            player.output("Number %d play of %s" % (i, o['card'].name))
            player.playCard(o['card'], discard=False, costAction=False)
        player.addCard(o['card'], 'played')
        player.hand.remove(o['card'])


###############################################################################
class Test_Kingscourt(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["King's Court", 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g["King's Court"].remove()

    def test_play(self):
        self.plr.setDeck('Estate', 'Estate', 'Gold', 'Gold', 'Duchy', 'Duchy')
        self.plr.setHand('Moat', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['play moat']
        self.plr.playCard(self.card)
        # (moat + 2) * 3 + estate
        self.assertEqual(self.plr.handSize(), 2 * 3 + 1)
        self.assertEqual(self.plr.playedSize(), 2)
        for c in self.plr.played:
            if c.name == 'Moat':
                break
        else:   # pragma: no cover
            self.fail("Didn't put moat in played")
        for c in self.plr.played:
            if c.name == "King's Court":
                break
        else:   # pragma: no cover
            self.fail("Didn't put moat in played")

    def test_noactions(self):
        self.plr.setHand('Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)

    def test_picked_nothing(self):
        """ Selected no actions with Kings court """
        self.plr.setHand('Estate', 'Estate', 'Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ["don't play"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
