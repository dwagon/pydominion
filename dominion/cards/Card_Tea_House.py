#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tea_House"""
import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Tea_House(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Sun; +1 Card; +1 Action; +$2"""
        self.name = "Tea House"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.coin = 2


###############################################################################
class Test_Tea_House(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Tea House"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tea House")

    def test_play(self) -> None:
        """Play card -"""
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(hand_size + 1, len(self.plr.piles[Piles.HAND]))
        self.assertEqual(actions, self.plr.actions.get())
        self.assertEqual(coins + 2, self.plr.coins.get())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
