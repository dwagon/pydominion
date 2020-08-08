#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Mystic(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DARKAGES
        self.desc = "+2 coin, +1 action; Name a card. Reveal the top card of your deck. If it's the named card, put it into your hand."
        self.name = 'Mystic'
        self.actions = 1
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """" Name a card. Reveal the top card of your deck. If it's
            the named card, put it into your hand """
        options = [{'selector': '0', 'print': 'No guess', 'card': None}]
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({'selector': sel, 'print': "Guess %s" % c.name, 'card': c})
            index += 1
        o = player.userInput(options, "Guess the top card")
        if not o['card']:
            return
        c = player.nextCard()
        player.revealCard(c)
        if o['card'].name == c.name:
            player.output("You guessed correctly")
            player.addCard(c, 'hand')
        else:
            player.output("You chose poorly - it was a %s" % c.name)
            player.addCard(c, 'topdeck')


###############################################################################
class Test_Mystic(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Mystic'], badcards=['Tournament', "Fool's Gold", "Pooka"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Mystic'].remove()

    def test_play(self):
        """ No guess should still get results """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_good(self):
        """ When the guess is good the card should move to the hand """
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Province')
        self.plr.test_input = ['Province']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertTrue(self.plr.in_hand('Province'))
        self.assertTrue(self.plr.deck.is_empty())

    def test_bad(self):
        """ When the guess is bad the card should stay on the deck """
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Province')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertTrue(not self.plr.in_hand('Gold'))
        self.assertTrue(not self.plr.in_hand('Province'))
        self.assertEqual(self.plr.deck[-1].name, 'Province')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
