#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Harbinger(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.EMPIRES
        self.desc = "+1 Card; +1 Action; Look through your discard pile. You may put a card from it onto your deck."
        self.name = 'Harbinger'
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game, player):
        index = 1
        options = [{'selector': '0', 'print': "Don't look through discard pile", 'card': None}]
        already = []
        for c in player.discardpile:
            sel = "{}".format(index)
            pr = "Put {} back in your deck".format(c.name)
            if c.name in already:
                continue
            options.append({'selector': sel, 'print': pr, 'card': c})
            already.append(c.name)
            index += 1
        if not already:
            player.output("No suitable cards")
            return
        player.output("Look through your discard pile. You may put a card from it onto your deck.")
        o = player.userInput(options, "Which Card? ")
        if not o['card']:
            return
        player.addCard(o['card'], 'topdeck')
        player.discardpile.remove(o['card'])


###############################################################################
class Test_Harbinger(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Harbinger'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Harbinger'].remove()

    def test_play(self):
        """ Play a harbinger """
        self.plr.setDiscard('Gold', 'Silver', 'Province')
        self.plr.test_input = ['Put Gold']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertIsNone(self.plr.in_discard('Gold'))
        self.assertIsNotNone(self.plr.in_deck('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
