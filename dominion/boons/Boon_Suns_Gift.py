#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Boon_Suns_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "Look at the top 4 cards of your deck. Discard any number of them and put the rest back in any order."
        )
        self.name = "The Sun's Gift"
        self.purchasable = False

    def special(self, game, player):
        cards = []
        for _ in range(4):
            c = player.next_card()
            if c:
                cards.append(c)
        todisc = player.plr_discard_cards(
            prompt="Discard any number and the rest go back on the top of the deck",
            any_number=True,
            cardsrc=cards,
        )
        for card in cards:
            if card not in todisc:
                player.add_card(card, "topdeck")


###############################################################################
class Test_Suns_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Sun's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_suns_gift(self):
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province", "Duchy", "Copper")
        self.plr.test_input = ["Province", "Duchy", "finish"]
        self.plr.play_card(self.card)
        try:
            self.assertIn("Silver", self.plr.piles[Piles.DECK])
            self.assertIn("Gold", self.plr.piles[Piles.DECK])
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Province"])
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Duchy"])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
