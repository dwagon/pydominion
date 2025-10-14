#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Practice"""
import unittest

from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Practice(Event.Event):
    """Practice"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.name = "Practice"
        self.desc = """You may play an Action card from your hand twice."""
        self.cost = 3

    def special(self, game, player):
        """You may play an Action card from your hand twice."""
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:  # pragma: no coverage
            player.output("No suitable actions to perform")
            return
        if cards := player.card_sel(cardsrc=actions):
            card = cards[0]
            for i in range(1, 3):
                player.output(f"Number {i} play of {card}")
                player.play_card(card, discard=False, cost_action=False)


###############################################################################
class TestPractice(unittest.TestCase):
    """Test Practice"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Practice"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Practice"]

    def test_play(self):
        """Use Practice twice"""
        self.plr.coins.set(3)
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        self.plr.test_input = ["Moat"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.perform_event(self.card)
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])

        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 4 - 1)  # Moat * 2


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
