#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Ironmonger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 card, +1 action. Reveal the top card of your deck; you may
        discard it.  Either way, if it is an... Action card, +1 Action;
        Treasure Card, +1 coin; Victory Card, +1 card"""
        self.name = 'Iron Monger'
        self.cost = 4
        self.actions = 1
        self.cards = 1

    def special(self, game, player):
        """ Reveal the top card of your deck; you may discard it.
            Either way, if it is an... Action card, +1 Action; Treasure
            Card, +1 coin; Victory Card, +1 card """
        card = player.nextCard()
        player.revealCard(card)
        ans = player.plrChooseOptions(
            "What to do with %s" % card.name,
            ('Put back %s' % card.name, False),
            ('Discard %s' % card.name, True)
        )
        if ans:
            player.discardCard(card)
        else:
            player.addCard(card, 'topdeck')
        if card.isVictory():
            player.output("Picking up card as %s was a victory card" % card.name)
            player.pickupCard()
        if card.isAction():
            player.output("Gaining action as %s was an action card" % card.name)
            player.addActions(1)
        if card.isTreasure():
            player.output("Gaining a coin as %s was a treasure card" % card.name)
            player.addCoin(1)


###############################################################################
class Test_Ironmonger(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Iron Monger'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.im = self.g['Iron Monger'].remove()
        self.plr.addCard(self.im, 'hand')

    def test_play(self):
        self.plr.test_input = ['put back']
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.get_actions(), 1)
        # 5 for hand, +1 for ironmonger and another potential +1 for action
        self.assertIn(self.plr.hand.size(), [6, 7])

    def test_victory(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Duchy', 'Estate')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.hand.size(), 7)

    def test_treasure(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Copper', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_action(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Iron Monger', 'Iron Monger')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_discard(self):
        self.plr.test_input = ['discard']
        self.plr.setDeck('Iron Monger', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.discardpile[0].name, 'Iron Monger')

    def test_putback(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Copper', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.deck[0].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
