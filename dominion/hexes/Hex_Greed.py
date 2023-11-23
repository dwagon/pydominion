#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex, Player, NoCardException


###############################################################################
class Hex_Greed(Hex.Hex):
    def __init__(self) -> None:
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a Copper onto your deck."
        self.name = "Greed"
        self.purchasable = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Copper", Piles.DECK)
        except NoCardException:
            player.output("No more Copper")


###############################################################################
class TestGreed(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Greed":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self) -> None:
        self.plr.piles[Piles.DECK].set("Duchy", "Cursed Village", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Cursed Village"])
        self.assertIn("Copper", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
