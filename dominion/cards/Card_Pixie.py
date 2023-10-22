#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Pixie(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card; +1 Action; Discard the top Boon. You may trash this to receive that Boon twice."
        self.name = "Pixie"
        self.cost = 2
        self.actions = 1
        self.cards = 1
        self.heirloom = "Goat"

    def special(self, game, player):
        topboon = game.receive_boon()
        opt = player.plr_choose_options(
            "Either:",
            (f"Discard {topboon.name}", False),
            (
                f"Trash Pixie to get {topboon.name} twice ({topboon.description(player)})",
                True,
            ),
        )
        if opt:
            player.trash_card(self)
            player.receive_boon(boon=topboon, discard=False)
            player.receive_boon(boon=topboon)


###############################################################################
class Test_Pixie(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pixie"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pixie")

    def test_play_keep(self):
        """Play a Pixie"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard The"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_trash(self):
        """Play a Pixie and trash it"""
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
            for c in self.plr.piles[Piles.DISCARD]:
                self.assertEqual(c.name, "Silver")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
