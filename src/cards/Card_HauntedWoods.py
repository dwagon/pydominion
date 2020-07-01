#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_HauntedWoods(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'duration']
        self.base = 'adventure'
        self.desc = """Until you next turn, when any other player buys a card, he puts his hand on top of his deck in any order.
        At the start of your next turn: +3 Cards"""
        self.name = 'Haunted Woods'
        self.cost = 5

    def duration(self, game, player):
        player.pickupCards(3)

    def hook_allPlayers_buyCard(self, game, player, owner, card):
        if player == owner:
            return
        if player.hasDefense(owner):
            return
        player.output("%s's Haunted Woods puts your hand onto your deck" % owner.name)
        for card in player.hand[:]:
            player.addCard(card, 'topdeck')
            player.hand.remove(card)
            player.output("Moving %s to deck" % card.name)


###############################################################################
class Test_HauntedWoods(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Haunted Woods'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Haunted Woods'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_buy(self):
        """ Play a Haunted Woods """
        self.vic.setHand('Silver', 'Duchy', 'Province')
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.vic.buyCard(self.g['Gold'])
        self.assertIsNotNone(self.vic.inDeck('Silver'))
        self.assertIsNotNone(self.vic.inDeck('Duchy'))
        self.assertIsNotNone(self.vic.inDeck('Province'))
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
