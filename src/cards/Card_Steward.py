#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Steward(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Choose: +2 cards, +2 coin, trash 2 cards"
        self.name = 'Steward'
        self.cost = 3

    def special(self, game, player):
        """ Choose one: +2 Cards; or +2 coin, or trash 2 cards from your hand """
        choice = player.plrChooseOptions(
            "Choose one?",
            ('+2 cards', 'cards'), ('+2 coin', 'coin'), ('Trash 2', 'trash'))
        if choice == 'cards':
            player.pickupCards(2)
            return
        if choice == 'coin':
            player.addCoin(2)
            return
        if choice == 'trash':
            player.output("Trash two cards")
            num = min(2, player.handSize())
            player.plrTrashCard(num=num, force=True)
            return


###############################################################################
class Test_Steward(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['steward'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['steward'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_cards(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_gold(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_trash(self):
        self.plr.test_input = ['2', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.g.trashSize(), 2)
        self.assertEqual(self.plr.handSize(), 3)

    def test_trash_smallhand(self):
        """ Trash two when there are less than two to trash """
        self.plr.setHand('copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['2', '1', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.g.trashSize(), 1)
        self.assertEqual(self.plr.handSize(), 0)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
