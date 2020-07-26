#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Watchtower(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.desc = """Draw until you have 6 cards in hand.
        When you gain a card, you may reveal this from your hand. If you do, either trash that card, or put it on top of your deck."""
        self.name = 'Watchtower'
        self.cost = 3

    def special(self, game, player):
        """ Draw until you have 6 cards in hand. """
        player.pickUpHand(6)

    def hook_gain_card(self, game, player, card):
        """ When you gain a card, you may reveal this from your
            hand. If you do, either trash that card, or put it on top
            of your deck """
        act = player.plrChooseOptions(
            "What to do with Watchtower?",
            ("Do nothing", 'nothing'),
            ("Trash %s" % card.name, 'trash'),
            ("Put %s on top of deck" % card.name, 'topdeck'))
        if act == 'trash':
            options = {'trash': True}
        elif act == 'topdeck':
            options = {'destination': 'topdeck'}
        else:
            options = {}
        return options


###############################################################################
class Test_Watchtower(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Watchtower'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Watchtower'].remove()

    def test_play(self):
        """ Play a watch tower """
        self.plr.setHand('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)

    def test_react_nothing(self):
        """ React to gaining a card - but do nothing """
        self.plr.setHand('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['nothing']
        self.plr.gainCard('Copper')
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.handSize(), 2)

    def test_react_trash(self):
        """ React to gaining a card - discard card"""
        tsize = self.g.trashSize()
        try:
            self.plr.test_input = ['trash']
            self.plr.setHand('Gold')
            self.plr.addCard(self.card, 'hand')
            self.plr.gainCard('Copper')
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertEqual(self.g.trashpile[-1].name, 'Copper')
            self.assertEqual(self.plr.handSize(), 2)
            self.assertEqual(self.plr.inHand('Copper'), None)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_react_topdeck(self):
        """ React to gaining a card - put card on deck"""
        tsize = self.g.trashSize()
        self.plr.test_input = ['top']
        self.plr.setHand('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.gainCard('Silver')
        try:
            self.assertEqual(self.g.trashSize(), tsize)
            self.assertEqual(self.plr.handSize(), 2)
            self.assertEqual(self.plr.inHand('Silver'), None)
            c = self.plr.nextCard()
            self.assertEqual(c.name, 'Silver')
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
