#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Famine"""
import unittest

from dominion import Card, Game, Piles, Hex, NoCardException, Player


###############################################################################
class Hex_Famine(Hex.Hex):
    """Famine"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Reveal the top 3 cards of your deck. Discard the Actions. Shuffle the rest into your deck."
        self.name = "Famine"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Reveal the top 3 cards of your deck. Discard the Actions. Shuffle the rest into your deck."""
        for _ in range(3):
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no coverage
                continue
            if card.isAction():
                player.output(f"Discarding {card}")
                player.discard_card(card)
            else:
                player.output(f"Putting {card} back in deck")
                player.add_card(card, Piles.DECK)
        player.piles[Piles.DECK].shuffle()


###############################################################################
class TestFamine(unittest.TestCase):
    """Test Famine"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Famine":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self):
        """Test playing"""
        self.plr.piles[Piles.DECK].set("Duchy", "Moat", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
