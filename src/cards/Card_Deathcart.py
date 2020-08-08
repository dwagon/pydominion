#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Deathcart(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.LOOTER]
        self.base = Game.DARKAGES
        self.desc = """You may trash an Action card from your hand. If you don't, trash this.
        When you gain this, gain two Ruins."""
        self.name = 'Death Cart'
        self.coin = 5
        self.cost = 4

    def special(self, game, player):
        action_cards = [c for c in player.hand if c.isAction()]
        trash = None
        if action_cards:
            trash = player.plrTrashCard(cardsrc=action_cards)
        if not trash:
            player.output("Didn't trash action - so trashing this card")
            player.trashCard(self)

    def hook_gain_this_card(self, game, player):
        for _ in range(2):
            c = player.gainCard('Ruins')
            player.output("Gained %s" % c.name)
        return {}


###############################################################################
class Test_Deathcart(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Death Cart', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Death Cart'].remove()

    def test_play(self):
        """ Play a death cart - no actions """
        tsize = self.g.trashSize()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Death Cart'))

    def test_play_trash(self):
        """ Play a death cart - no actions """
        tsize = self.g.trashSize()
        self.plr.setHand('Copper', 'Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Moat'))
        self.assertIsNone(self.g.in_trash('Death Cart'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
