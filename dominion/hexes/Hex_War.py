#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_War(Hex.Hex):
    """War"""

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
            card = player.next_card()
            if not card:
                break
            player.reveal_card(card)
            if card.cost in (3, 4):
                player.output(f"Trashing {card.name}")
                player.trash_card(card)
                break
            player.output(f"Discarding {card.name}")
            player.discard_card(card)
            count -= 1
        else:
            player.output("No cards costing 3 or 4 in deck")


###############################################################################
class Test_War(unittest.TestCase):
    """Test War"""

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
