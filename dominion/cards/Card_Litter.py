#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Litter"""

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Litter(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "+2 Cards; +2 Actions; +1 Debt"
        self.name = "Litter"
        self.cost = 5
        self.cards = 2
        self.actions = 2

    def special(self, game: "Game.Game", player: "Player.Player"):
        player.debt.add(1)


###############################################################################
class Test_Litter(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Litter"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Litter")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        debt = self.plr.debt.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.debt.get(), debt + 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 1)  # -1 for card played
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
