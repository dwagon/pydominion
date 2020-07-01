#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Wishingwell(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 Card +1 Action; Name a card, then reveal the top card of your deck. If it's the named card, put it into your hand."
        self.name = 'Wishing Well'
        self.actions = 1
        self.cards = 1
        self.cost = 3

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
class Test_Wishingwell(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Wishing Well'], badcards=["Fool's Gold", "Tournament", "Pooka"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Wishing Well'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ No guess still gets a card and action """
        self.plr.test_input = ['no guess']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 6)

    def test_good(self):
        """ A good guess means the card ends up in the hand"""
        self.plr.setDeck('Silver', 'Copper')
        self.plr.test_input = ['Silver']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.inHand('Silver'))

    def test_bad(self):
        """ Guessing badly should result in the card staying on the deck """
        self.plr.setDeck('Province', 'Copper')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.assertTrue(not self.plr.inHand('Gold'))
        self.assertTrue(not self.plr.inHand('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
