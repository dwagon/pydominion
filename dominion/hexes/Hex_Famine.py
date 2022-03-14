#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_Famine(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = "Reveal the top 3 cards of your deck. Discard the Actions. Shuffle the rest into your deck."
        self.name = "Famine"
        self.purchasable = False

    def special(self, game, player):
        for _ in range(3):
            c = player.next_card()
            if c.isAction():
                player.output("Discarding {}".format(c))
                player.discard_card(c)
            else:
                player.output("Putting {} back in deck".format(c))
                player.add_card(c, "topdeck")
        player.deck.shuffle()


###############################################################################
class Test_Famine(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Famine":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self):
        self.plr.set_deck("Duchy", "Cursed Village", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertIsNotNone(self.plr.in_discard("Cursed Village"))
        self.assertIsNotNone(self.plr.in_deck("Gold"))
        self.assertIsNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
