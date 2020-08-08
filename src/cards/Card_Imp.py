#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Imp(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'spirit']
        self.base = 'nocturne'
        self.desc = "+2 Cards; You may play an Action card from your hand that you don't have a copy of in play."
        self.name = "Imp"
        self.purchasable = False
        self.insupply = False
        self.cards = 2
        self.cost = 2
        self.numcards = 13

    def special(self, game, player):
        # Get action cards in hand
        ac = [_ for _ in player.hand if _.isAction()]
        if not ac:
            player.output("No action cards")
            return
        # Select ones that haven't been played
        sac = [_ for _ in ac if not player.in_played(_.name)]
        if not sac:
            player.output("No unplayed action cards")
            return
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        index = 1
        for p in sac:
            selector = "{}".format(index)
            toprint = 'Play {} ({})'.format(p.name, p.description(player))
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1
        o = player.userInput(options, "What card do you want to play?")
        if o['card']:
            player.playCard(o['card'], costAction=False)


###############################################################################
class Test_Imp(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Imp", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Imp"].remove()

    def test_played(self):
        self.plr.setHand("Moat", "Copper")
        self.plr.addCard(self.card, 'hand')
        self.plr.setPlayed("Moat")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2 + 2)

    def test_not_played(self):
        self.plr.setHand("Moat", "Copper")
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2 + 2 + 1)    # 2 for moat, 2 for imp, 1 for hand


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
