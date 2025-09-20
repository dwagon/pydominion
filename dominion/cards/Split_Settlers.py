#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Settlers(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Settlers"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.desc = """+1 Card; +1 Action. Look through your discard pile.
                    You may reveal a Copper from it and put it into your hand."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if discarded_copper := player.piles[Piles.DISCARD]["Copper"]:
            player.move_card(discarded_copper, Piles.HAND)
            player.reveal_card(discarded_copper)
            player.output("Pulled Copper from discard into hand")
        else:
            player.output("No Copper in discard")


###############################################################################
class Test_Settlers(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Settlers"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Settlers")

    def test_play(self) -> None:
        """Play a Settlers and pull a copper"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertNotIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1 + 1)

    def test_play_no_copper(self) -> None:
        """Play a Settlers and pull no copper"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver")
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Duchy")
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
