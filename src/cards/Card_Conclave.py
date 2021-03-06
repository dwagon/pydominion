#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Conclave(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION]
        self.base = Game.NOCTURNE
        self.desc = "+2 Coin; You may play an Action card from your hand that you don't have a copy of in play. If you do, +1 Action."
        self.name = 'Conclave'
        self.cost = 4
        self.coin = 2

    def special(self, game, player):
        ac = [_ for _ in player.hand if _.isAction()]
        if not ac:
            player.output("No actions to play")
            return
        sac = [_ for _ in ac if not player.in_played(_.name)]
        if not sac:
            player.output("No suitable actions to play")
            return
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        index = 1
        for p in sac:
            selector = "{}".format(index)
            toprint = 'Play {}'.format(p.name)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1
        o = player.userInput(options, "What card do you want to play?")
        if o['card']:
            player.playCard(o['card'], costAction=False)
            player.addActions(1)


###############################################################################
class Test_Conclave(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Conclave', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Conclave'].remove()

    def test_played(self):
        self.plr.setHand("Moat", "Copper")
        self.plr.addCard(self.card, 'hand')
        self.plr.setPlayed("Moat")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_not_played(self):
        self.plr.setHand("Moat", "Copper")
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
