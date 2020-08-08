#!/usr/bin/env python

import unittest
import Game
from Card import Card


class Card_Alchemist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+2 cards, +1 action; When you discard this you may put on top of your deck if you have a Potion in play"
        self.name = 'Alchemist'
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = True
        self.required_cards = ['Potion']

    def hook_discardThisCard(self, game, player, source):
        """ When you discard this from play, you may put this on
            top of your deck if you have a Potion in play """
        # As we can't guarantee where we are in the discard cycle
        # We have to check the discardpile as well
        if source != 'played':
            return
        if not player.inPlayed('Potion') and not player.in_discard('Potion'):
            return
        ans = player.plrChooseOptions(
            'What to do with the alchemist?',
            ('Discard alchemist', False), ('Put on top of deck', True))
        if ans:
            alc = player.inPlayed('Alchemist')
            if alc:
                player.played.remove(alc)
            else:
                alc = player.in_discard('Alchemist')
                if alc:
                    player.discardpile.remove(alc)
            player.addCard(self, 'topdeck')


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Alchemist'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.alchemist = self.g['Alchemist'].remove()
        self.plr.addCard(self.alchemist, 'hand')

    def test_play(self):
        self.plr.playCard(self.alchemist)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 7)

    def test_nopotion(self):
        """ Discard Alchemist with no potion in play """
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(self.plr.discard_size(), 8)  # 5 for hand, +2 cards, alch

    def test_discard(self):
        """ Discard an Alchemist even if we have a potion in play """
        self.plr.setPlayed('Potion')
        self.plr.test_input = ['discard']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(self.plr.discard_size(), 9)  # 5 for hand, +2 cards, alch, pot
        self.assertIsNotNone(self.plr.in_discard('Alchemist'))

    def test_keep(self):
        """ Keep an Alchemist for next turn """
        self.plr.setPlayed('Potion')
        self.plr.test_input = ['top of deck']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertIsNone(self.plr.in_discard('Alchemist'))
        self.assertEqual(self.plr.deck[-1].name, 'Alchemist')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
