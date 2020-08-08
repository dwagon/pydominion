#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Lurker(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.INTRIGUE
        self.desc = "+1 Action; Choose one: Trash an Action card from the Supply, or gain an Action card from the trash."
        self.name = 'Lurker'
        self.cost = 2
        self.actions = 1

    def special(self, game, player):
        ch = player.plrChooseOptions(
            "Choose one? ",
            ("Trash an Action from the Supply", 'to'),
            ("Gain an Action card from the Trash", 'from')
        )
        if ch == 'to':
            acts = [_ for _ in game.cardpiles.values() if _.isAction() and not _.is_empty()]
            if not acts:
                player.output("No suitable cards found")
                return
            cards = player.cardSel(cardsrc=acts, prompt="Select Action from Supply to Trash")
            card = game[cards[0].name].remove()
            player.addCard(card, 'played')   # In order to trash
            player.trashCard(card)
        if ch == 'from':
            acts = [_ for _ in game.trashpile if _.isAction()]
            if not acts:
                player.output("No suitable cards found")
                return
            card = player.cardSel(cardsrc=acts, prompt="Select Action from the Trash")
            game.trashpile.remove(card[0])
            player.addCard(card[0], 'discard')


###############################################################################
class Test_Lurker(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Lurker', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Lurker'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_trash(self):
        self.plr.test_input = ['Trash an Action', 'Moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Moat'))
        self.assertEqual(self.plr.get_actions(), 0 + 1)

    def test_recover(self):
        self.plr.test_input = ['Gain an Action', 'Moat']
        self.g.set_trash('Moat')
        self.plr.playCard(self.card)
        self.assertIsNone(self.g.in_trash('Moat'))
        self.assertIsNotNone(self.plr.in_discard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
