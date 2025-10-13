#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Adventurer"""
import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Adventurer(Card.Card):
    """Adventurer"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = """Reveal cards from your deck until you reveal 2 Treasure cards.
            Put those Treasure cards into your hand and discard the other revealed cards."""
        self.name = "Adventurer"
        self.cost = 6

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal cards from your deck until you reveal two treasure cards
        Add those to your hand and discard the other revealed cards"""
        treasures: list[Card.Card] = []
        max_cards = player.count_cards()
        count = 0
        while len(treasures) < 2 and count <= max_cards:
            count += 1
            try:
                card = player.pickup_card(verbose=False)
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isTreasure():
                treasures.append(card)
                player.output(f"Adding {card}")
            else:
                player.discard_card(card)
                player.output(f"Discarding {card} as not treasure")


###############################################################################
class TestAdventurer(unittest.TestCase):
    """Test Adventurer"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Adventurer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Adventurer")

    def test_treasures(self) -> None:
        """Play card"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Estate")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(
            sorted(["Silver", "Gold"]),
            sorted([_.name for _ in self.plr.piles[Piles.HAND]]),
        )
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Estate"])
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
