#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game


###############################################################################
class Boon_Moons_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.TYPE_BOON
        self.base = Game.NOCTURNE
        self.desc = (
            "Look through your discard pile. You may put a card from it onto your deck"
        )
        self.name = "The Moon's Gift"
        self.purchasable = False

    def special(self, game, player):
        if not player.discardpile.size():
            return
        cards = []
        cardnames = set()
        for c in player.discardpile:
            if c.name not in cardnames:
                cards.append(c)
                cardnames.add(c.name)
        card = player.card_sel(
            cardsrc=cards, prompt="Pull card from discard and add to top of your deck"
        )
        player.add_card(card[0], "topdeck")
        player.discardpile.remove(card[0])


###############################################################################
class Test_Moons_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Moon's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()

    def test_moons_gift(self):
        self.plr.discardpile.set("Province", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.deck[-1].name, "Gold")
        self.assertNotIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
