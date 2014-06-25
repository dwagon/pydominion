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
        self.purchasable = False
        self.cost = 0

    def special(self, game, player):
        """ You may trash 2 cards from your hand. If you do, +2
            cards, +2 gold, and each other player discards down to 3
            cards in hand """

        ans = player.plrChooseOptions(
            "Trash cards?",
            ('Trash nothing', False), ('Trash 2 cards', True))
        if not ans:
            return
        player.plrTrashCard(2, force=True)
        player.pickupCards(2)
        player.addGold(2)
        for plr in player.attackVictims():
            plr.plrDiscardDownTo(3)


###############################################################################
class Test_Mercenary(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['mercenary', 'moat'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['mercenary'].remove()

    def test_play(self):
        """ Trash nothing with mercenary - should do nothing """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.victim.discardpile, [])

    def test_defense(self):
        """ Make sure moats work against mercenaries """
        self.plr.addCard(self.card, 'hand')
        moat = self.g['moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.test_input = ['1', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), 2)
        self.assertEqual(self.plr.handSize(), 5)
        # 5 for hand + moat
        self.assertEqual(self.victim.handSize(), 6)
        self.assertEqual(self.victim.discardpile, [])

    def test_attack(self):
        """ Attack with a mercenary """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '1', '2', '0']
        self.victim.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), 2)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getGold(), 2)
        self.assertEqual(self.victim.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
