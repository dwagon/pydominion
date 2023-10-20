#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Prosper"""
import unittest
from dominion import Card, Game, Event, Piles


###############################################################################
class Event_Prosper(Event.Event):
    """Prosper"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = " Gain a Loot, plus any number of differently named Treasures."
        self.name = "Prosper"
        self.cost = 10
        self.required_cards = ["Loot"]

    def special(self, game, player):
        """Gain a Loot, plus any number of differently named Treasures."""
        player.gain_card("Loot")
        treasures = [game.card_instances[_] for _ in game.get_treasure_piles()]
        to_gain = player.card_sel(anynum=True, cardsrc=treasures)
        for card in to_gain:
            player.gain_card(card.name)


###############################################################################
class TestProsper(unittest.TestCase):
    """Test Prosper"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Prosper"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Prosper"]

    def test_play(self):
        """Perform a Prosper"""
        self.plr.coins.add(10)
        self.plr.test_input = ["Select Gold", "Finish"]
        self.plr.perform_event(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertTrue(any(True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
