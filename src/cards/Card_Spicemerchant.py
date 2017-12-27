#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_SpiceMerchant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = """You may trash a Treasure from your hand. If you do, choose one: +2 Cards and +1 Action; or +2 Coins and +1 Buy."""
        self.name = 'Spice Merchant'
        self.cost = 4

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        tr = player.plrTrashCard(prompt="Trash a treasure from your hand for +2 Cards, +1 Action / +2 Coins, +1 Buy", cardsrc=treasures)
        if tr:
            rew = player.plrChooseOptions(
                "Select your reward",
                ("+2 Cards, +1 Action", 'cards'),
                ("+2 Coins, +1 Buy", 'coins'))
            if rew == 'cards':
                player.pickupCards(2)
                player.addActions(1)
            else:
                player.addCoin(2)
                player.addBuys(1)


###############################################################################
class Test_SpiceMerchant(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Spice Merchant'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Spice Merchant'].remove()

    def test_play_card(self):
        """ Play an Spice Merchant and select cards"""
        tsize = self.g.trashSize()
        self.plr.setHand('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold', 'cards']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.inTrash('Gold'))
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_play_coins(self):
        """ Play an Spice Merchant and select coins"""
        tsize = self.g.trashSize()
        self.plr.setHand('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold', 'coins']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.inTrash('Gold'))
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
