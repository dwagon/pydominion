#!/usr/bin/env python

import unittest
from dominion import Boon, Card, Game, Piles, Player, NoCardException


###############################################################################
class Boon_Mountains_Gift(Boon.Boon):
    def __init__(self) -> None:
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a silver"
        self.name = "The Mountain's Gift"
        self.purchasable = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Silver")
        except NoCardException:
            player.output("No more Silvers")


###############################################################################
class Test_Mountains_Gift(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break
        self.card = self.g.get_card_from_pile("Bard")

    def test_mountains_gift(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
