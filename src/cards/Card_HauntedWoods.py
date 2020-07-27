#!/usr/bin/env python

import unittest
import Game
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
        for crd in player.hand[:]:
            player.addCard(crd, 'topdeck')
            player.hand.remove(crd)
            player.output("Moving %s to deck" % crd.name)


###############################################################################
class Test_HauntedWoods(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Haunted Woods'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Haunted Woods'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_buy(self):
        """ Play a Haunted Woods """
        self.vic.setHand('Silver', 'Duchy', 'Province')
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.vic.setCoin(6)
        self.vic.buyCard(self.g['Gold'])
        self.assertIsNotNone(self.vic.in_deck('Silver'))
        self.assertIsNotNone(self.vic.in_deck('Duchy'))
        self.assertIsNotNone(self.vic.in_deck('Province'))
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.handSize(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
