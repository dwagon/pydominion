#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Courtyard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+3 cards. Put a card from your hand on top of your deck."
        self.name = 'Courtyard'
        self.cards = 3
        self.cost = 2

    def special(self, game, player):
        """ Put a card from your hand on top of your deck """
        cards = player.cardSel(prompt='Put which card on top of deck?', num=1, verbs=('Put', 'Unput'))
        if not cards:
            return
        card = cards[0]
        player.addCard(card, 'topdeck')
        player.hand.remove(card)
        player.output("Put %s on top of deck" % card.name)


###############################################################################
class Test_Courtyard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Courtyard'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.cy = self.g['Courtyard'].remove()

    def test_play(self):
        """ Play courtyard """
        self.plr.addCard(self.cy, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.cy)
        self.assertEqual(self.plr.hand.size(), 8)

    def test_putcard(self):
        """ Use courtyard to put a card to the top of the deck """
        self.plr.setHand('Gold')
        self.plr.addCard(self.cy, 'hand')
        self.plr.test_input = ['put gold']
        self.plr.playCard(self.cy)
        card = self.plr.nextCard()
        self.assertEqual(card.name, 'Gold')
        for c in self.plr.hand:
            self.assertNotEqual(c.name, 'Gold')
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
