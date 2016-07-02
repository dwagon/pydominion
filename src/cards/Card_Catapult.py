#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Catapult(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.required_cards = ['Curse']
        self.base = 'empires'
        self.desc = """+1 Coin; Trash a card from your hand.
        If it costs 3 or more, each other player gains a Curse.
        If it's a Treasure, each other player discards down to 3 cards in hand."""
        self.name = 'Catapult'
        self.cost = 3
        self.coin = 1

    def special(self, game, player):
        cards = player.plrTrashCard()
        card = cards[0]
        for plr in player.attackVictims():
            if card.cost >= 3:
                plr.output("%s's Catapult Curses you" % player.name)
                plr.gainCard('Curse')
            if card.isTreasure():
                plr.output("%s's Catapult forces you to discard down to 3 cards" % player.name)
                plr.plrDiscardDownTo(3)


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Catapult(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Catapult'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['Catapult'].remove()

    def test_play(self):
        """ Play a Catapult with a non-treasure"""
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNotNone(self.g.inTrash('Duchy'))
        self.assertIsNotNone(self.victim.inDiscard('Curse'))

    def test_play_treasure(self):
        """ Play a Catapult with a treasure"""
        self.plr.setHand('Copper')
        self.victim.test_input = ['1', '2', '0']
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.inTrash('Copper'))
        self.assertEqual(self.victim.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
