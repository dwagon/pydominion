#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Hermit"""
import unittest

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Hermit(Card.Card):
    """Hermit"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Look through your discard pile. You may trash a non-Treasure from it or from your hand.
            Gain a card costing up to $3. At the end of your Buy phase this turn, if you didn't gain any cards in it,
            exchange this for a Madman."""
        self.name = "Hermit"
        self.required_cards = [("Card", "Madman")]
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Look through your discard pile. You may trash a non-Treasure
        from it or from your hand. Gain a card costing up to $3."""
        to_trash = [_ for _ in player.piles[Piles.DISCARD] + player.piles[Piles.HAND] if not _.isTreasure()]
        player.plr_trash_card(cardsrc=to_trash, prompt="Trash one of these?")
        # Gain a card costing up to 3.
        player.plr_gain_card(3)

    def hook_end_buy_phase(self, game: "Game.Game", player: "Player.Player") -> None:
        """At the end of your Buy phase this turn, if you didn't gain any cards in it
        exchange this for a Madman."""
        if player.stats["gained"]:
            return
        player.replace_card(self, "Madman")


###############################################################################
class TestHermit(unittest.TestCase):
    """Test Hermit"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Hermit"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hermit")

    def test_play_discard(self) -> None:
        """Play a Hermit trashing card from discard"""
        self.plr.piles[Piles.DISCARD].set("Province", "Gold")
        self.plr.test_input = ["trash province", "get silver"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertNotIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_hand(self) -> None:
        """Play a Hermit trashing card from hand"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.test_input = ["trash province", "get silver"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_discard(self) -> None:
        """Discard a Hermit and gain a Madman"""
        self.plr.test_input = ["End Phase"]
        self.plr.add_card(self.card, Piles.PLAYED)
        self.plr.buy_phase()
        self.plr.discard_hand()
        self.assertIn("Madman", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Hermit", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
