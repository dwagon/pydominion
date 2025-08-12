#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Rustic_Village"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Rustic_Village(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Sun; +1 Card; +2 Actions; You may discard 2 cards for +1 Card."""
        self.name = "Rustic Village"
        self.cost = 4
        self.cards = 1
        self.actions = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may discard 2 cards for +1 Card."""
        cards = player.plr_discard_cards(num=2)
        if len(cards) == 2:
            player.pickup_card()


###############################################################################
class Test_Rustic_Village(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Rustic Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Rustic Village")

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
