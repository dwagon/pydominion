#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Scepter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'renaissance'
        self.desc = "When you play this, choose one: 2 coin; or replay an Action card you played this turn that's still in play."
        self.name = 'Scepter'
        self.cost = 5

    def special(self, game, player):
        acts = [_ for _ in player.played if _.isAction()]
        if acts:
            get_coin = player.plrChooseOptions(
                "Pick one? ",
                ("2 Coin", True),
                ("Replay an action card", False)
            )
        else:
            get_coin = True
            player.output("No suitable cards - gaining coin")
        if get_coin:
            player.addCoin(2)
        else:
            player.output("acts={}".format(acts))
            card = player.cardSel(cardsrc=acts)
            player.addCard(card[0], 'hand')
            player.played.remove(card[0])
            player.playCard(card[0], costAction=False)


###############################################################################
class Test_Scepter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Scepter', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Scepter'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_coin(self):
        self.plr.test_input = ["2 Coin"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_play_replay(self):
        self.plr.setPlayed('Moat')
        self.plr.test_input = ["Replay", "Moat"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.handSize(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
