#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Butcher(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+2 special coins - trash a card to buy a card"
        self.name = 'Butcher'
        self.cost = 5

    def special(self, game, player):
        """ Take 2 Coin tokens. You may trash a card from your hand
            and then pay any number of Coin tokens. If you did trash a
            card, gain a card with a cost up to the cost of the trashed
        card play the number of Coin tokens you paid """
        player.gainSpecialCoins(2)
        trash = player.plrChooseOptions(
            'Trash a card to buy a card?',
            ("Don't trash cards", False), ('Trash a card', True))
        if not trash:
            return
        card = player.plrTrashCard(force=True)[0]
        options = []
        for i in range(player.getSpecialCoins() + 1):
            sel = '%d' % i
            options.append({'selector': sel, 'print': 'Add %d coins' % i, 'coins': i})
        o = player.userInput(options, "Spend extra coins?")
        cost = card.cost + o['coins']
        player.trashCard(card)
        player.specialcoins -= o['coins']
        player.plrGainCard(cost=cost)


###############################################################################
class Test_Butcher(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['butcher'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['butcher'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a butcher"""
        self.plr.specialcoins = 0
        self.plr.test_input = ["Don't trash"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getSpecialCoins(), 2)

    def test_trash_gold(self):
        """ Trash a gold """
        self.plr.setHand('copper', 'gold', 'silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.specialcoins = 0
        # Trash a card
        # Trash card 3
        # Spend 2 coin
        # Buy card 1
        self.plr.test_input = ['trash a card', 'trash gold', 'add 2', 'get silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getSpecialCoins(), 0)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.discardSize(), 1)
        for m in self.plr.messages:
            if 'Province' in m:
                break
        else:   # pragma: no cover
            self.fail("Couldn't get a province for 8")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
