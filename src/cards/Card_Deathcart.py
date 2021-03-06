#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Deathcart(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LOOTER]
        self.base = Game.DARKAGES
        self.desc = """You may trash this or an Action card from your hand, for +5 Coin.
            When you gain this, gain 2 Ruins."""
        self.name = 'Death Cart'
        self.cost = 4

    def special(self, game, player):
        action_cards = [c for c in player.hand if c.isAction()]
        choices = [
            ("Trash this Death Cart for 5 Gold", 'trash_dc'),
            ]
        if action_cards:
            choices.append(("Trash an Action card for 5 Gold", 'trash_action'))
        else:
            choices.append(("No action cards to trash", 'nothing'))
        choices.append(("Do nothing", 'nothing'))
        ans = player.plrChooseOptions("What to do with Death Cart?", *choices)
        trash = None
        if ans == 'nothing':
            return
        if ans == 'trash_action':
            trash = player.plrTrashCard(cardsrc=action_cards)
        if ans == 'trash_dc':
            player.output("Trashing Death Cart")
            player.trashCard(self)
            trash = True
        if trash:
            player.addCoin(5)

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
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Do nothing']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNone(self.g.in_trash('Death Cart'))

    def test_play_trash_action(self):
        """ Play a death cart - no actions """
        self.plr.setHand('Copper', 'Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash an Action', 'Trash Moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertIsNotNone(self.g.in_trash('Moat'))
        self.assertIsNone(self.g.in_trash('Death Cart'))

    def test_play_trash_self(self):
        """ Play a death cart - no actions """
        self.plr.setHand('Copper', 'Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash this Death']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertIsNone(self.g.in_trash('Moat'))
        self.assertIsNotNone(self.g.in_trash('Death Cart'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
