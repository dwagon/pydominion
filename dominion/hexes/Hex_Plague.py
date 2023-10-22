#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex


###############################################################################
class Hex_Plague(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a Curse to your hand."
        self.name = "Plague"
        self.purchasable = False
        self.required_cards = ["Curse"]

    def special(self, game, player):
        player.gain_card("Curse", destination=Piles.HAND)


###############################################################################
class Test_Plague(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Plague":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_plague(self):
        self.plr.piles[Piles.DECK].set("Duchy", "Cursed Village", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertIn("Curse", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
