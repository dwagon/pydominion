#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Scholar(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """Discard your hand. +7 Cards."""
        self.name = "Scholar"
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.discard_hand()
        player.pickup_cards(7)


###############################################################################
class TestScholar(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Scholar"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Scholar")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
