#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex


###############################################################################
class Hex_BadOmens(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Put your deck into your discard pile. Look through it and put 2 Coppers from it onto your deck"
        self.name = "Bad Omens"
        self.purchasable = False

    def special(self, game, player):
        for card in player.piles[Piles.DECK]:
            player.add_card(card, Piles.DISCARD)
            player.piles[Piles.DECK].remove(card)
        numcu = 0
        for card in player.piles[Piles.DISCARD]:
            if card.name == "Copper":
                numcu += 1
                player.add_card(card, Piles.DECK)
                player.piles[Piles.DISCARD].remove(card)
                if numcu == 2:
                    break


###############################################################################
class Test_BadOmens(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Bad Omens":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Silver", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].count("Copper"), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
