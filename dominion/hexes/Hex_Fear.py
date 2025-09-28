#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Fear"""
import unittest

from dominion import Card, Game, Piles, Hex, Player


###############################################################################
class Hex_Fear(Hex.Hex):
    """Fear"""

    def __init__(self) -> None:
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """If you have at least 5 cards in hand, discard an Action or Treasure"""
        self.name = "Fear"
        self.purchasable = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """If you have at least 5 cards in hand, discard an Action or Treasure"""
        if player.piles[Piles.HAND].size() < 5:
            return
        t_and_a = [_ for _ in player.piles[Piles.HAND] if _.isAction() or _.isTreasure()]
        player.plr_discard_cards(num=1, cardsrc=t_and_a, prompt="Discard an Action or a Treasure")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    """Discard a treasure - should never have an action"""
    return player.pick_to_discard(1, keepvic=True)


###############################################################################
class Test_Fear(unittest.TestCase):
    """Test Fear"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Fear":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_not_enough(self) -> None:
        """Test having fewer than 5"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)  # The Cursed Village

    def test_fear(self) -> None:
        """Test discarding"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Estate", "Duchy", "Copper")
        self.plr.test_input = ["Copper"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
