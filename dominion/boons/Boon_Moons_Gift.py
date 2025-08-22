#!/usr/bin/env python

import unittest

from dominion import Boon, Card, Game, Piles, Player


###############################################################################
class Boon_Moons_Gift(Boon.Boon):
    def __init__(self) -> None:
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Look through your discard pile. You may put a card from it onto your deck"
        self.name = "The Moon's Gift"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if not player.piles[Piles.DISCARD].size():
            return
        cards = []
        card_names = set()
        for c in player.piles[Piles.DISCARD]:
            if c.name not in card_names:
                cards.append(c)
                card_names.add(c.name)
        if card := player.card_sel(cardsrc=cards, prompt="Pull card from discard and add to top of your deck"):
            player.move_card(card[0], Piles.TOPDECK)


###############################################################################
class TestMoonsGift(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Moon's Gift":
                self.g.boons = [b]
                break
        self.card = self.g.get_card_from_pile("Bard")

    def test_moons_gift(self) -> None:
        self.plr.piles[Piles.DISCARD].set("Province", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
