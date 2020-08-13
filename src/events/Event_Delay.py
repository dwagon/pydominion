#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Delay(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'menagerie'
        self.desc = """You may set aside an Action card from your hand. At the
            start of your next turn, play it."""
        self.name = "Delay"
        self.cost = 0

    def special(self, game, player):
        actions = []
        for card in player.hand:
            if card.isAction():
                actions.append(card)
        if not actions:
            player.output("No actions to delay")
            return
        delay = player.cardSel(
            prompt="Set aside an action card to play next turn",
            cardsrc=actions
        )
        player.defer_card(delay[0])
        player.hand.remove(delay[0])


###############################################################################
class Test_Delay(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Delay'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events['Delay']

    def test_play(self):
        """ Perform a Delay """
        self.plr.test_input = ['Select Moat']
        self.plr.setHand('Moat', 'Copper', 'Estate')
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_defer('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
