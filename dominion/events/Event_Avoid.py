#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Avoid"""

import unittest

from dominion import Game, Event, Card, Player, Piles, PlayArea

AVOID = "avoid"


###############################################################################
class Event_Avoid(Event.Event):
    """Avoid"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Buy; The next time you shuffle this turn, pick up to 3 of
            those cards to put into your discard pile."""
        self.name = "Avoid"
        self.cost = 2
        self.buys = 1

    def hook_pre_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        player.specials[AVOID] = PlayArea.PlayArea(initial=[])
        cards = player.card_sel(num=3, cardsrc=Piles.DISCARD, prompt="Pick up to 3 cards to put into discard pile")
        for card in cards:
            player.move_card(card, player.specials[AVOID])
            player.secret_count += 1

    def hook_post_shuffle(self, game: "Game.Game", player: "Player.Player"):
        if AVOID in player.specials:
            for card in player.specials[AVOID]:
                player.move_card(card, Piles.DISCARD)
                player.secret_count -= 1
            del player.specials[AVOID]


###############################################################################
class TestAvoid(unittest.TestCase):
    """Test Avoid"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Avoid"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Avoid"]

    def test_play(self) -> None:
        """Perform  Avoid"""
        self.plr.coins.add(2)
        buys = self.plr.buys.get()
        self.plr.piles[Piles.HAND].set("Copper", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.test_input = ["Select Estate", "Select Duchy", "Select Province", "Finish"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.buys.get(), buys)  # +1 for Avoid, -1 for playing event
        self.plr.end_turn()
        self.g.print_state()
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 3)
        self.assertNotIn("Province", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertNotIn("Province", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
