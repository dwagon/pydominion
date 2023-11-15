#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Talisman(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 coin. Gain copy of non-victory cards you buy"
        self.name = "Talisman"
        self.playable = False
        self.cost = 4
        self.coin = 1

    def hook_buy_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> None:
        """While this is in play, when you buy a card costing 4
        or less that is not a victory card, gain a copy of it."""
        if card.cost <= 4 and not card.isVictory():
            try:
                if new_card := game.get_card_from_pile(card.pile):
                    player.output(f"Gained another {card} from Talisman")
                    player.add_card(new_card)
            except NoCardException:
                player.output(f"No more {card} in supply")


###############################################################################
class TestTalisman(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Talisman"], oldcards=True, badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Talisman")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy(self) -> None:
        self.plr.play_card(self.card)
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Copper")

    def test_too_expensive(self) -> None:
        self.plr.play_card(self.card)
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Gold")

    def test_victory(self) -> None:
        self.plr.play_card(self.card)
        self.plr.coins.set(6)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
