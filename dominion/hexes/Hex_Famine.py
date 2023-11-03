#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex, NoCardException


###############################################################################
class Hex_Famine(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Reveal the top 3 cards of your deck. Discard the Actions. Shuffle the rest into your deck."
        self.name = "Famine"
        self.purchasable = False

    def special(self, game, player):
        for _ in range(3):
            try:
                card = player.next_card()
            except NoCardException:
                continue
            if card.isAction():
                player.output(f"Discarding {card}")
                player.discard_card(card)
            else:
                player.output(f"Putting {card} back in deck")
                player.add_card(card, "topdeck")
        player.piles[Piles.DECK].shuffle()


###############################################################################
class TestFamine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Famine":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self):
        self.plr.piles[Piles.DECK].set("Duchy", "Cursed Village", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Cursed Village"])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
