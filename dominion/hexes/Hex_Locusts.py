#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex, Player, NoCardException


###############################################################################
class Hex_Locusts(Hex.Hex):
    def __init__(self) -> None:
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Trash the top card of your deck. If it's Copper or Estate,
            gain a Curse. Otherwise, gain a cheaper card that shares a type with it."""
        self.name = "Locusts"
        self.purchasable = False
        self.required_cards = ["Curse"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            nxt = player.top_card()
        except NoCardException:
            return
        if nxt.name in ("Copper", "Estate"):
            player.output(f"Gaining a curse because your next card is {nxt}")
            try:
                player.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")
        else:
            player.output(
                f"Gain a card costing {nxt.cost - 1} because your next card is {nxt}"
            )
            types = {
                Card.CardType.VICTORY: nxt.isVictory(),
                Card.CardType.TREASURE: nxt.isTreasure(),
                Card.CardType.ACTION: nxt.isAction(),
            }
            player.plr_gain_card(cost=nxt.cost - 1, types=types)
        player.output(f"Trashing your {nxt}")
        player.trash_card(nxt)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if "Silver" in [_.name for _ in kwargs["cardsrc"]]:
        return ["Silver"]
    if "Duchy" in [_.name for _ in kwargs["cardsrc"]]:
        return ["Duchy"]
    if "Copper" in [_.name for _ in kwargs["cardsrc"]]:
        return ["Copper"]
    if "Estate" in [_.name for _ in kwargs["cardsrc"]]:
        return ["Estate"]
    return [kwargs["cardsrc"][0].name]


###############################################################################
class TestLocusts(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Locusts":
                self.g.hexes.remove(h)

    def test_curse(self) -> None:
        """Locusts to gain a Curse"""
        self.plr.piles[Piles.DECK].set("Estate")
        self.plr.gain_card("Cursed Village")
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Curse"])
        self.assertIn("Estate", self.g.trash_pile)

    def test_gain(self) -> None:
        """Locusts to gain a cheaper card"""
        self.plr.piles[Piles.DECK].set("Duchy")
        self.plr.test_input = ["Get Estate"]
        self.plr.gain_card("Cursed Village")
        self.assertNotIn("Curse", self.plr.piles[Piles.DISCARD])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Estate"])
        self.assertIn("Duchy", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
