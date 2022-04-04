#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Experiment(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.name = "Experiment"
        self.desc = """+2 Cards; +1 Action; Return this to the Supply. When you
            gain this, gain another Experiment (that doesn't come with another)."""
        self.cost = 3
        self.cards = 2
        self.actions = 1

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.gain_card("Experiment", callhook=False)
        player.output("Gained a new experiment")

    ###########################################################################
    def special(self, game, player):
        player.played.remove(self)
        game[self.name].add(self)
        player.output("Returned experiment to stack")


###############################################################################
class Test_Experiment(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Experiment"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.card = self.g["Experiment"].remove()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 0 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_gain_card(self):
        self.plr.gain_card("Experiment")
        count = 0
        for card in self.plr.discardpile:
            if card.name == "Experiment":
                count += 1
        self.assertEqual(count, 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
