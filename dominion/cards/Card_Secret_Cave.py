#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Secret_Cave"""
import unittest

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_SecretCave(Card.Card):
    """Secret Cave"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+1 Card; +1 Action; You may discard 3 cards. If you did,
            then at the start of your next turn, +$3."""
        self.name = "Secret Cave"
        self.cost = 3
        self.actions = 1
        self.cards = 1
        self.heirloom = "Magic Lamp"
        self._discarded = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        dcs = player.plr_discard_cards(num=3, prompt="If you discard 3 cards next turn gain 3 Coin")
        if dcs:
            self._discarded = True

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        if self._discarded:
            player.output("Gained 3 Coin from Secret Cave")
            player.coins.add(3)
        return {}


###############################################################################
class TestSecretCave(unittest.TestCase):
    """Test Secret Cave"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Secret Cave"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Secret Cave")

    def test_play_keep(self):
        """Play a Secret Cave"""
        self.plr.piles[Piles.HAND].set("Silver", "Estate", "Duchy", "Province", "Copper")
        self.plr.test_input = [
            "Discard Silver",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.actions.get(), 1)
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1 - 3)
            self.plr.end_turn()
            self.plr.start_turn()
            self.assertEqual(self.plr.coins.get(), 3)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
