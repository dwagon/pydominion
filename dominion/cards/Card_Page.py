#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, PlayArea


###############################################################################
class Card_Page(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Card, +1 Action; Discard to replace with Treasure Hunter"
        self.name = "Page"
        self.traveller = True
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def hook_discard_this_card(
        self, game: Game.Game, player: Player.Player, source: PlayArea.PlayArea
    ) -> None:
        """Replace with Treasure Hunter"""
        player.replace_traveller(self, "Treasure Hunter")


###############################################################################
class Test_Page(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Page")

    def test_page(self) -> None:
        """Play a page"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
