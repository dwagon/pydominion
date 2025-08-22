#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Alley"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Alley(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SHADOW]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Card. +1 Action. Discard a card."""
        self.name = "Alley"
        self.cost = 4
        self.cards = 1
        self.actions = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Discard a card."""
        player.plr_discard_cards(1, force=True)


###############################################################################
class Test_Alley(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Alley"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Alley")

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.DECK].set("Duchy", "Province", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        self.plr.test_input = ["Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1 - 2)  # -2 for play and discard
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
