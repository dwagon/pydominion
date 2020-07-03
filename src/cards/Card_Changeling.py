#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Changeling(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night']
        self.base = 'nocturne'
        self.desc = """Trash this. Gain a copy of a card you have in play.
In games using this, when you gain a card costing 3 or more, you may exchange it for a Changeling."""
        self.name = 'Changeling'
        self.cost = 3

    def hook_gainCard(self, game, player, card):
        if card.cost < 3:
            return
        if game['Changeling'].isEmpty():
            return
        swap = player.plrChooseOptions(
            "Swap {} for a Changeling?".format(card.name),
            ("Swap {}".format(card.name), True),
            ("Keep {}".format(card.name), False)
            )
        if swap:
            return {'replace': 'Changeling'}

    def night(self, game, player):
        options = [{'selector': '0', 'print': "Keep Changeling", 'card': None}]
        index = 1
        for card in player.played + player.hand:
            sel = "{}".format(index)
            pr = "Exchange for {}".format(card.name)
            options.append({'selector': sel, 'print': pr, 'card': card})
            index += 1
        o = player.userInput(options, "Trash Changeling to gain a card")
        if o['card']:
            player.trashCard(self)
            player.gainCard(o['card'].name)


###############################################################################
class Test_Changeling(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Changeling'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Changeling'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_keep(self):
        self.plr.phase = 'night'
        self.plr.test_input = ['Keep Changeling']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inPlayed('Changeling'))

    def test_play_swap(self):
        self.plr.phase = 'night'
        self.plr.setPlayed('Gold')
        self.plr.test_input = ['Exchange for Gold']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.g.in_trash('Changeling'))

    def test_gain_keep(self):
        self.plr.test_input = ['Keep Silver']
        self.plr.gainCard('Silver')
        self.assertIsNotNone(self.plr.inDiscard('Silver'))

    def test_gain_swap(self):
        self.plr.test_input = ['Swap Silver']
        self.plr.gainCard('Silver')
        self.assertIsNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Changeling'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
