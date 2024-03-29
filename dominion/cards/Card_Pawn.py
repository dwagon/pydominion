#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Pawn(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "Choose two: +1 card, +1 action, +1 buy, +1 coin"
        self.name = "Pawn"
        self.cost = 2

    def special(self, game, player):
        """Choose two: +1 card; +1 action +1 buy; +1 coin. (The
        choices must be different)"""
        selectable = [
            ("card", "+1 card"),
            (Card.CardType.ACTION, "+1 action"),
            ("buy", "+1 buy"),
            ("coin", "+1 coin"),
        ]
        chosen = []
        player.output("Pick two options")
        for _ in range(2):
            options = []
            index = 1
            for k, v in selectable:
                if k in chosen:
                    continue
                options.append({"selector": f"{index}", "print": v, "opt": k})
                index += 1
            o = player.user_input(options, "What do you want to do?")
            chosen.append(o["opt"])

        for choice in chosen:
            if choice == "card":
                player.pickup_cards(1)
            elif choice == Card.CardType.ACTION:
                player.add_actions(1)
            elif choice == "buy":
                player.buys.add(1)
            elif choice == "coin":
                player.coins.add(1)


###############################################################################
class Test_Pawn(unittest.TestCase):
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
