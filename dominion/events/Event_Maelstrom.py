#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Maelstrom"""
import unittest
from dominion import Card, Game, Event, Piles


###############################################################################
class Event_Maelstrom(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Trash 3 cards from your hand. Each other player with 5 or more cards in hand trashes one of them."
        self.name = "Maelstrom"
        self.cost = 4

    def special(self, game, player):
        player.plr_trash_card(num=3)
        for victim in player.attack_victims():
            if len(victim.piles[Piles.HAND]) >= 5:
                victim.output(f"{player.name}'s Maelstrom forces you to trash a card")
                victim.plr_trash_card(num=1, force=1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Trash in order of usefulness
    for card_name in ["Copper", "Silver", "Estate", "Duchy", "Gold", "Province"]:
        if card_name in player.piles[Piles.HAND]:
            return [player.piles[Piles.HAND][card_name]]


###############################################################################
class TestMaelstrom(unittest.TestCase):
    """Test Maelstrom"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, events=["Maelstrom"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.events["Maelstrom"]

    def test_play(self):
        self.plr.coins.add(4)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        self.victim.piles[Piles.HAND].set("Estate", "Copper", "Silver", "Gold", "Duchy")
        self.plr.test_input = ["Trash Copper", "Finish"]
        self.victim.test_input = ["Trash Gold"]
        self.plr.perform_event(self.card)
        self.g.print_state()
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
