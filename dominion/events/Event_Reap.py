#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Reap"""
import unittest

from dominion import Card, Game, Piles, Event, PlayArea, Player, OptionKeys

REAP = "reap"


###############################################################################
class Event_Reap(Event.Event):
    """Reap"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain a Gold. Set it aside. If you do, at the start of your next turn, play it."""
        self.name = "Reap"
        self.cost = 7

    def special(self, game: Game.Game, player: Player.Player) -> None:
        gold = player.gain_card("Gold")
        player.specials[REAP] = PlayArea.PlayArea("Reap", game)
        player.move_card(gold, player.specials[REAP])
        player.secret_count += 1

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        if REAP not in player.specials:
            return {}
        for card in player.specials[REAP]:
            player.play_card(card, cost_action=False)
            player.secret_count -= 1
        player.specials[REAP].empty()
        return {}


###############################################################################
class TestReap(unittest.TestCase):
    """Test Reap"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Reap"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Reap"]

    def test_rush(self) -> None:
        """Use Reap"""
        self.plr.coins.set(7)
        self.plr.perform_event(self.event)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
