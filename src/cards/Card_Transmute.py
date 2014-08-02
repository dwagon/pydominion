#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Transmute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Trash a card from hand to gain others"
        self.name = 'Transmute'
        self.cost = 0
        self.potcost = 1

    def special(self, game, player):
        """ Trash a card from your hand. If it is an...
            Action card, gain a Duchy, Treasure card, gain a Transmute,
            Victory card, gain a gold """
        player.output("Trash a card to gain...")
        options = []
        options.append({'selector': '0', 'print': 'Trash Nothing', 'card': None, 'gain': None})
        index = 1
        for c in player.hand:
            sel = "%d" % index
            if c.isAction():
                trashtag = 'Duchy'
            elif c.isTreasure():
                trashtag = 'Transmute'
            elif c.isVictory():
                trashtag = 'Gold'
            pr = "Trash %s for %s" % (c.name, trashtag)
            options.append({'selector': sel, 'print': pr, 'card': c, 'gain': trashtag})
            index += 1
        o = player.userInput(options, "Trash which card?")
        if not o['card']:
            return
        player.trashCard(o['card'])
        if o['gain'] != 'Nothing':
            player.gainCard(o['gain'])


###############################################################################
class Test_Transmute(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['transmute'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['transmute'].remove()

    def test_play(self):
        """ Play a transmute - trash nothing """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash nothing']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_trash_treasure(self):
        """ Transmute a treasure card to gain a Transmute """
        self.plr.setHand('gold', 'estate', 'transmute')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Transmute')

    def test_trash_action(self):
        """ Transmute a action card to gain a Duchy """
        self.plr.setHand('gold', 'estate', 'transmute')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash transmute']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Duchy')

    def test_trash_victory(self):
        """ Transmute a victory card to gain a Gold """
        self.plr.setHand('gold', 'estate', 'transmute')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash estate']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Gold')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
