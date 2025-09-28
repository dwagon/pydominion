#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Bad_Omens"""
import unittest

from dominion import Card, Game, Piles, Hex, Player


###############################################################################
class Hex_Bad_Omens(Hex.Hex):
    """Bad Omens"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Put your deck into your discard pile. Look through it and put 2 Coppers from it onto your deck"
        self.name = "Bad Omens"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Put your deck into your discard pile. Look through it and put 2 Coppers from it onto your deck"""
        for card in player.piles[Piles.DECK]:
            player.move_card(card, Piles.DISCARD)
        num_cu = 0
        for card in player.piles[Piles.DISCARD]:
            if card.name == "Copper":
                num_cu += 1
                player.move_card(card, Piles.DECK)
                if num_cu == 2:
                    break


###############################################################################
class Test_Bad_Omens(unittest.TestCase):
    """Test Bad Omens"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Bad Omens":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        """Test Play"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Silver", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].count("Copper"), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
