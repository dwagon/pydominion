#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Fishmonger"""
import unittest

from dominion import Game, Card


###############################################################################
class Card_Fishmonger(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SHADOW]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Buy; +$1"""
        self.name = "Fishmonger"
        self.cost = 2
        self.buys = 1
        self.coin = 1


###############################################################################
class Test_Fishmonger(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Fishmonger"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fishmonger")

    def test_play(self) -> None:
        """Play card"""
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()

        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
