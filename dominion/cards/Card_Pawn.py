#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Pawn"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Pawn(Card.Card):
    """Pawn"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """Choose two: +1 Card; +1 Action; +1 Buy; +$1. The choices must be different."""
        self.name = "Pawn"
        self.cost = 2

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Choose two: +1 card; +1 action +1 buy; +1 coin. (The
        choices must be different)"""
        selectable = [
            ("card", "+1 card"),
            ("action", "+1 action"),
            ("buy", "+1 buy"),
            ("coin", "+1 coin"),
        ]
        chosen = []
        player.output("Pick two options")
        for _ in range(2):
            choices = []
            for k, v in selectable:
                if k in chosen:
                    continue
                choices.append((v, k))
            choice = player.plr_choose_options("What do you want to do?", *choices)
            chosen.append(choice)

        for choice in chosen:
            if choice == "card":
                player.pickup_cards(1)
            elif choice == "action":
                player.add_actions(1)
            elif choice == "buy":
                player.buys.add(1)
            elif choice == "coin":
                player.coins.add(1)


###############################################################################
class TestPawn(unittest.TestCase):
    """Test Pawn"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pawn"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pawn")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play the pawn - select card and action"""
        self.plr.test_input = ["+1 card", "+1 action"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_play_buy(self):
        """Play the pawn - select buy and coin"""
        self.plr.test_input = ["+1 buy", "+1 coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
