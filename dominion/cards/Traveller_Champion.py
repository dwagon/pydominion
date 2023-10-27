#!/usr/bin/env python

import unittest
from typing import Optional

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Champion(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "For the rest of the game +1 Action / Action; Defense"
        self.name = "Champion"
        self.permanent = True
        self.purchasable = False
        self.defense = True
        self.numcards = 5
        self.cost = 6

    def hook_post_play(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> Optional[dict[str, str]]:
        if card.isAction():
            player.add_actions(1)
        return None


###############################################################################
class TestChampion(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Page", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Champion")

    def test_champion(self) -> None:
        """Play a champion"""
        self.plr.add_card(self.card, Piles.DURATION)
        self.assertEqual(self.plr.actions.get(), 1)
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
