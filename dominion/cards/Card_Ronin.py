#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Ronin"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Ronin(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SHADOW]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Draw until you have 7 cards in hand."""
        self.name = "Ronin"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Draw until you have 7 cards in hand."""
        to_pickup = 7 - len(player.piles[Piles.HAND])
        player.pickup_cards(to_pickup)


###############################################################################
class Test_Ronin(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Ronin"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Ronin")

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
