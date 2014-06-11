#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Steward(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Choose: +2 cards, +2 gold, trash 2 cards"
        self.name = 'Steward'
        self.cost = 3

    def special(self, game, player):
        """ Choose one: +2 Cards; or +2 gold, or trash 2 cards from your hand """
        options = [
            {'selector': '1', 'print': '+2 Cards', 'choose': 'cards'},
            {'selector': '2', 'print': '+2 Gold', 'choose': 'gold'},
            {'selector': '3', 'print': 'Trash 2', 'choose': 'trash'}
        ]
        o = player.userInput(options, "Choose one?")
        if o['choose'] == 'cards':
            player.pickupCards(2)
            return
        if o['choose'] == 'gold':
            player.t['gold'] += 2
            return
        if o['choose'] == 'trash':
            player.output("Trash two cards")
            num = min(2, len(player.hand))
            player.plrTrashCard(num=num, force=True)
            return


###############################################################################
class Test_Steward(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['steward'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['steward'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_cards(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 7)
        self.assertEqual(self.plr.t['gold'], 0)

    def test_gold(self):
        self.plr.test_input = ['2']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.t['gold'], 2)

    def test_trash(self):
        self.plr.test_input = ['3', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(len(self.g.trashpile), 2)
        self.assertEqual(len(self.plr.hand), 3)

    def test_trash_smallhand(self):
        """ Trash two when there are less than two to trash """
        self.plr.setHand('copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['3', '1', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(len(self.g.trashpile), 1)
        self.assertEqual(len(self.plr.hand), 0)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
