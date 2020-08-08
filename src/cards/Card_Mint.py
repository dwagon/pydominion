#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Mint(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.name = 'Mint'
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return """You may reveal a Treasure card from your hand. Gain a copy of it.
            When you buy this, trash all Treasures you have in play."""
        return "You may reveal a Treasure card from your hand. Gain a copy of it."

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        if not treasures:
            player.output("No treasures to reveal")
            return
        toget = player.cardSel(
            num=1,
            cardsrc=treasures,
            prompt="Reveal a treasure to gain a copy of"
            )
        player.revealCard(toget[0])
        if toget:
            player.output("Gained a %s from the Mint" % toget[0].name)
            player.gainCard(toget[0].name)

    def hook_buy_this_card(self, game, player):
        """ Trash all Treasures you have in play"""
        totrash = [c for c in player.played if c.isTreasure()]
        for c in totrash:
            player.output("Mint trashing %s" % c.name)
            player.trashCard(c)


###############################################################################
class Test_Mint(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Mint', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Mint'].remove()

    def test_play(self):
        self.plr.setHand('Duchy', 'Gold', 'Silver', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discard_size(), 1)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertIsNotNone(self.plr.inHand('Gold'))

    def test_buy(self):
        tsize = self.g.trashSize()
        self.plr.coin = 5
        self.plr.setHand('Gold', 'Estate')
        self.plr.setPlayed('Copper', 'Silver', 'Estate', 'Moat')
        self.plr.buyCard(self.g['Mint'])
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertIsNotNone(self.g.in_trash('Copper'))
        self.assertIsNotNone(self.g.in_trash('Silver'))
        self.assertIsNone(self.g.in_trash('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
