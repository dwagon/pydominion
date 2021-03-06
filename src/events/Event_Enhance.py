#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Enhance(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = """You may trash a non-Victory card from your hand,
            to gain a card costing up to 2 Coin more than it."""
        self.name = "Enhance"
        self.cost = 3

    def special(self, game, player):
        crds = [_ for _ in player.hand if not _.isVictory()]
        if not crds:
            player.output("No non-Victory cards available")
            return
        tc = player.plrTrashCard(
            prompt="Trash to gain a card costing 2 more than",
            printcost=True,
            cardsrc=crds
            )
        if not tc:
            return
        new_cost = tc[0].cost + 2
        player.plrGainCard(cost=new_cost, force=True)


###############################################################################
class Test_Enhance(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=['Enhance'],
            initcards=['Festival'], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events['Enhance']

    def test_play(self):
        """ Perform a Enhance """
        self.plr.addCoin(3)
        self.plr.setHand('Copper', 'Silver', 'Estate')
        self.plr.test_input = ['Trash Silver', 'Get Festival']
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.g.in_trash('Silver'))
        self.assertIsNotNone(self.plr.in_discard('Festival'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
