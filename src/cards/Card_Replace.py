#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Replace(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = """Trash a card from your hand. Gain a card costing up to 2 more
            than it. If the gained card is an Action or Treasure, put it onto your deck;
            if it's a Victory card, each other player gains a Curse."""
        self.name = 'Replace'
        self.required_cards = ['Curse']
        self.cost = 5

    def special(self, game, player):
        tr = player.plrTrashCard()
        if not tr:
            return
        cost = tr[0].cost
        gain = player.plrGainCard(cost, prompt="Gain a card costing up to {}".format(cost))
        if not gain:
            return
        if gain.isAction() or gain.isTreasure():
            player.addCard(gain, 'topdeck')
            player.discardpile.remove(gain)
        if gain.isVictory():
            for victim in player.attackVictims():
                victim.gainCard('Curse')


###############################################################################
class Test_Replace(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Replace', 'Moat'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Replace'].remove()

    def test_gain_action(self):
        self.plr.setHand('Estate', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Estate', 'Get Moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDeck('Moat'))
        self.assertIsNone(self.plr.inDiscard('Moat'))

    def test_gain_victory(self):
        self.plr.setHand('Estate', 'Silver',)
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Estate', 'Get Estate']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.vic.inDiscard('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
