#!/usr/bin/env python

import unittest
from Card import Card


class Card_Mercenary(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = "You may trash 2 cards for +2 cards, +2 gold other players discard down to 3"
        self.name = 'Mercenary'
        self.purcashable = False
        self.cost = 0

    def special(self, game, player):
        """ You may trash 2 cards from your hand. If you do, +2
            cards, +2 gold, and each other player discards down to 3
            cards in hand """

        options = [
            {'selector': '0', 'print': 'Trash nothing', 'trash': False},
            {'selector': '1', 'print': 'Trash 2 cards', 'trash': True}
        ]
        o = player.userInput(options, "Trash cards?")
        if not o['trash']:
            return
        player.plrTrashCard(2, force=True)
        for i in range(2):
            player.pickupCard()
        player.t['gold'] += 2
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense(player):
                continue
            plr.plrDiscardDownTo(3)


###############################################################################
class Test_Mercenary(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['mercenary', 'moat'])
        self.plr = self.g.players[0]
        self.victim = self.g.players[1]
        self.card = self.g['mercenary'].remove()

    def test_play(self):
        """ Trash nothing with mercenary - should do nothing """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.victim.discardpile, [])

    def test_defense(self):
        """ Make sure moats work against mercenaries """
        self.plr.addCard(self.card, 'hand')
        moat = self.g['moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.test_input = ['1', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.g.trashpile), 2)
        self.assertEqual(len(self.plr.hand), 5)
        # 5 for hand + moat
        self.assertEqual(len(self.victim.hand), 6)
        self.assertEqual(self.victim.discardpile, [])

    def test_attack(self):
        """ Attack with a mercenary """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '1', '2', '0']
        self.victim.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.g.trashpile), 2)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.t['gold'], 2)
        self.assertEqual(len(self.victim.hand), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
