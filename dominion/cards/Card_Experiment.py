#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys, NoCardException


###############################################################################
class Card_Experiment(Card.Card):
    def __init__(self) -> None:
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
    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        try:
            player.gain_card("Experiment", callhook=False)
            player.output("Gained a new experiment")
        except NoCardException:  # pragma: no coverage
            player.output("No more Experiments")
        return {}

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Return to supply"""
        # Sometimes the card will already be moved (e.g. Throne Room)
        if self in player.piles[Piles.HAND]:
            player.move_card(self, Piles.CARDPILE)
            player.output("Returned experiment to stack")


###############################################################################
class TestExperiment(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Experiment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        self.card = self.g.get_card_from_pile("Experiment")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_gain_card(self) -> None:
        self.plr.gain_card("Experiment")
        count = sum(1 for card in self.plr.piles[Piles.DISCARD] if card.name == "Experiment")
        self.assertEqual(count, 2)

    def test_gain_none_left(self) -> None:
        """Gain an experiment when there are no more left"""
        for _ in range(9):
            self.g.get_card_from_pile("Experiment")
        try:
            self.plr.gain_card("Experiment")
        except:
            self.fail("Failed when gaining experiment")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
