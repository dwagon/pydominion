#!/usr/bin/env python

import unittest
from Card import Card


class Card_Cultist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'looter']
        self.base = 'darkages'
        self.desc = "+2 cards, All others gain a ruin. Trash for +3 cards"
        self.name = 'Cultist'
        self.cost = 5
        self.cards = 2

    def special(self, game, player):
        """ Each other play gains a Ruins. You may play a Cultist
            from your hand. """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense(player):
                continue
            plr.gainCard('ruins')
        cultist = player.inHand('cultist')
        if cultist:
            options = [
                {'selector': '0', 'print': "Don't play cultist", 'play': False},
                {'selector': '1', 'print': "Play cultist", 'play': True}
            ]
            o = player.userInput(options, 'Play another cultist?')
            if o['play']:
                player.playCard(cultist, costAction=False)

    def hook_trashThisCard(self, game, player):
        """ When you trash this, +3 cards """
        for i in range(3):
            player.pickupCard()


###############################################################################
class Test_Cultist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['cultist', 'moat'])
        self.plr = self.g.players[0]
        self.victim = self.g.players[1]
        self.card = self.g['cultist'].remove()

    def test_play(self):
        """ Play a cultists - should give 2 cards """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 7)
        self.assertEqual(len(self.victim.discardpile), 1)
        self.assertTrue(self.victim.discardpile[0].isRuin())

    def test_defense(self):
        """ Make sure moats work against cultists """
        self.plr.addCard(self.card, 'hand')
        moat = self.g['moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 7)
        self.assertEqual(self.victim.discardpile, [])

    def test_noother(self):
        """ Don't ask to play another cultist if it doesn't exist """
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.test_input, ['0'])

    def test_anothercultist_no(self):
        """ Don't play the other cultist """
        self.plr.setHand('cultist', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.played), 1)

    def test_anothercultist_yes(self):
        """ Another cultist can be played for free """
        self.plr.setHand('cultist', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.played), 2)
        self.assertEqual(self.plr.t['actions'], 0)
        for c in self.plr.played:
            self.assertEqual(c.name, 'Cultist')
        self.assertEqual(len(self.victim.discardpile), 2)
        for c in self.victim.discardpile:
            self.assertTrue(c.isRuin())

    def test_trash(self):
        """ Trashing a cultist should give 3 more cards """
        self.plr.addCard(self.card, 'hand')
        self.plr.trashCard(self.card)
        self.assertEqual(self.g.trashpile[0].name, 'Cultist')
        self.assertEqual(len(self.plr.hand), 8)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
