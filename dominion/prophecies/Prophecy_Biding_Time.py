#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Biding_Time"""
import unittest

from dominion import Card, Game, Prophecy, Piles, Player, PlayArea

BIDING_TIME = "biding_time"


###############################################################################
class Prophecy_Biding_Time(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """At the start of your Clean-up, set aside your hand face down.
                At the start of your next turn, put those cards into your hand."""
        self.name = "Biding Time"

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if BIDING_TIME not in player.specials:
            player.specials[BIDING_TIME] = PlayArea.PlayArea(initial=[])
        for card in player.specials[BIDING_TIME]:
            player.move_card(card, Piles.HAND)
            player.output(f"Moving {card} back into hand")
            player.secret_count -= 1
            player.specials[BIDING_TIME] = PlayArea.PlayArea(initial=[])

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> None:
        if BIDING_TIME not in player.specials:
            player.specials[BIDING_TIME] = PlayArea.PlayArea(initial=[])
        for card in player.piles[Piles.HAND]:
            player.move_card(card, player.specials[BIDING_TIME])
            player.output(f"Biding Time setting aside {card}")
            player.secret_count += 1
        player.piles[Piles.HAND].empty()

    def debug_dump(self, player: Player.Player) -> None:
        if BIDING_TIME in player.specials:
            player.output(f"Biding Time Reserve: {self}: {player.specials[BIDING_TIME]}")


###############################################################################
class Test_Biding_Time(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Biding Time"], initcards=["Poet"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Copper", "Copper", "Copper")
        self.plr.piles[Piles.PLAYED].set("Silver", "Gold")
        self.plr.end_turn()
        self.plr.start_turn()
        self.g.print_state()
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Copper", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
