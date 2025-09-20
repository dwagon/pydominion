#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Pixie(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card; +1 Action; Discard the top Boon. You may trash this to receive that Boon twice."
        self.name = "Pixie"
        self.cost = 2
        self.actions = 1
        self.cards = 1
        self.heirloom = "Goat"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        top_boon = game.receive_boon()
        if not top_boon:
            player.output("No boons left")
            return
        if player.plr_choose_options(
            "Either:",
            (f"Discard {top_boon.name}", False),
            (
                f"Trash Pixie to get {top_boon.name} twice ({top_boon.description(player)})",
                True,
            ),
        ):
            player.trash_card(self)
            player.receive_boon(boon=top_boon, discard=False)
            player.receive_boon(boon=top_boon)


###############################################################################
class TestPixie(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Pixie"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pixie")

    def test_play_keep(self) -> None:
        """Play a Pixie"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard The"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_trash(self) -> None:
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
