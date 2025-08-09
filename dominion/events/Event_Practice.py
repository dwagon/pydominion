#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Practice(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.name = "Practice"
        self.desc = """You may play an Action card from your hand twice."""
        self.cost = 3

    def special(self, game, player):
        """You may play an Action card from your hand twice."""
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            player.output("No suitable actions to perform")
            return
        cards = player.card_sel(cardsrc=actions)
        if not cards:
            return
        card = cards[0]
        for i in range(1, 3):
            player.output(f"Number {i} play of {card}")
            player.play_card(card, discard=False, cost_action=False)


###############################################################################
class Test_Practice(unittest.TestCase):
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
        self.g.print_state()
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 0)
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 4)  # Moat * 2


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
