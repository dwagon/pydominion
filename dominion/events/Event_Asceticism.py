#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Asceticism"""
import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Asceticism(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.name = "Asceticism"
        self.cost = 2
        self.desc = """Pay any amount of $ to trash that many cards from your hand."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Pay any amount of $ to trash that many cards from your hand."""
        if player.coins.get() == 0:
            return
        while player.coins.get() > 0:
            if player.plr_trash_card(1):
                player.coins.add(-1)
            else:
                break


###############################################################################
class Test_Asceticism(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Asceticism"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Asceticism"]

    def test_play(self) -> None:
        """Use Asceticism"""
        self.plr.coins.set(4)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Duchy")
        self.plr.test_input = ["Trash Copper", "Trash Estate"]
        self.plr.perform_event(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
