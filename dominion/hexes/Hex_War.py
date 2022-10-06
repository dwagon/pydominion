#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_War(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Reveal cards from your deck until revealing one costing 3 or 4. Trash it and discard the rest."
        self.name = "War"
        self.purchasable = False

    def special(self, game, player):
        count = player.discardpile.size() + player.deck.size()
        while count:
            c = player.top_card()
            if not c:
                break
            if c.cost in (3, 4):
                player.output(f"Trashing {c.name}")
                player.trash_card(c)
                break
            player.output(f"Discarding {c.name}")
            player.discard_card(c)
            count -= 1
        else:
            player.output("No cards costing 3 or 4 in deck")


###############################################################################
class Test_War(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "War":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_war(self):
        tsize = self.g.trashpile.size()
        self.plr.deck.set("Duchy", "Cursed Village", "Silver")
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.g.trashpile.size(), tsize + 1)
        self.assertIn("Silver", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
