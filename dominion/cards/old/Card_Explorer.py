#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Explorer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.desc = """You may reveal a Province from your hand. If you do,
            gain a Gold to your hand. If you don't, gain a Silver to your hand."""
        self.name = "Explorer"
        self.base = Card.CardExpansion.SEASIDE
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if prov := player.piles[Piles.HAND]["Province"]:
            player.reveal_card(prov)
            try:
                player.gain_card("Gold", destination=Piles.HAND)
            except NoCardException:
                player.output("No more Gold")
        else:
            try:
                player.gain_card("Silver", destination=Piles.HAND)
            except NoCardException:
                player.output("No more Silver")


###############################################################################
class TestExplorer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Explorer"], oldcards=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Explorer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_province(self) -> None:
        self.plr.gain_card("Province", Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        # 5 + province + gold
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_no_province(self) -> None:
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
