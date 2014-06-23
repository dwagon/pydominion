#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = "Trash this and players with 5 or more cards discard a card of your choice"
        self.name = 'Pillage'
        self.needspoils = True
        self.cost = 5

    ###########################################################################
    def hook_trashThisCard(self, game, player):
        """ Trash this. Each other player with 5 or more cards in
            hand reveals his hand and discards a card that you choose.
            Gain 2 Spoils from the Spoils pile """
        for i in range(2):
            player.gainCard('Spoils')
        for plr in player.attackVictims():
            if plr.handSize() < 5:
                player.output("Player %s has too small a hand size" % plr.name)
                continue
            self.pickACard(plr, player)

    ###########################################################################
    def pickACard(self, victim, player):
        index = 1
        options = []
        for card in victim.hand:
            sel = '%d' % index
            options.append({'selector': sel, 'print': 'Discard %s' % card.name, 'card': card})
            index += 1
        o = player.userInput(options, "Which card to discard from %s" % victim.name)
        victim.discardCard(o['card'])
        victim.output("%s pillaged your %s" % (player.name, o['card'].name))


###############################################################################
class Test_Pillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['pillage', 'moat'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['pillage'].remove()

    def test_play(self):
        """ Nothing should happen """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getGold(), 0)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_defended(self):
        """ Victim has a defense """
        self.plr.hand = []
        self.plr.addCard(self.card, 'hand')
        moat = self.g['moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Spoils')
        self.assertEqual(self.victim.handSize(), 6)

    def test_nohandsize(self):
        """ Victim has too small a hand"""
        self.plr.hand = []
        self.victim.setHand('copper', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Spoils')
        self.assertEqual(self.victim.handSize(), 2)

    def test_attack(self):
        """ Victim has no defense and a large enough hand """
        self.plr.hand = []
        self.plr.test_input = ['1']
        self.victim.setHand('copper', 'copper', 'copper', 'copper', 'gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Spoils')
        self.assertEqual(self.victim.handSize(), 4)
        self.assertEqual(self.victim.discardSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
