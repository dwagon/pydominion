#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_Haunting(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "If you have at least 4 cards in hand, put one of them onto your deck."
        self.name = "Haunting"
        self.purchasable = False

    def special(self, game, player):
        if player.hand.size() >= 4:
            card = player.card_sel(force=True)
            player.add_card(card[0], "topdeck")
            player.hand.remove(card[0])


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1)


###############################################################################
class Test_Haunting(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Haunting":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_none(self):
        self.plr.hand.set("Duchy", "Gold", "Silver")
        self.plr.gain_card("Cursed Village")

    def test_activate(self):
        self.plr.hand.set("Duchy", "Gold", "Silver", "Province")
        self.plr.test_input = ["Gold"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.deck[-1].name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
