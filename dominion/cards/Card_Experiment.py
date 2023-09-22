#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Experiment(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
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
        player.move_card(self, game.card_piles["Experiment"])
        player.output("Returned experiment to stack")


###############################################################################
class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Experiment"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.card = self.g.get_card_from_pile("Experiment")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_gain_card(self):
        self.plr.gain_card("Experiment")
        count = 0
        for card in self.plr.piles[Piles.DISCARD]:
            if card.name == "Experiment":
                count += 1
        self.assertEqual(count, 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
