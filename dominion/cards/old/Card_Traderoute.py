#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Trade_Route"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_TradeRoute(Card.Card):
    """Trade Route"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 Buy; Trash a card from your hand. +1 Coin per Coin token on the Trade Route mat."
        self.name = "Trade Route"
        self.cost = 3
        self.buys = 1

    @classmethod
    def setup(cls, game: Game.Game) -> None:
        """Setup: Add a Coin token to each Victory Supply pile; move that token
        to the Trade Route mat when a card is gained from the pile."""
        cls.tokens = {}
        cls.game = game
        for name, card_pile in game.get_card_piles():
            card = game.card_instances[name]
            if card.isVictory():
                cls.tokens[name] = len(card_pile)

    def is_worth(self, game: Game.Game) -> int:
        worth = 0
        for name, card_pile in game.get_card_piles():
            if name in self.tokens and self.tokens[name] != len(card_pile):
                worth += 1
        return worth

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+1 coin per token on the trade route map. Trash a card
        from your hand."""
        player.plr_trash_card()
        player.coins.add(self.is_worth(game))


###############################################################################
class TestTradeRoute(unittest.TestCase):
    """Test Trade Route"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Trade Route"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.trade_route = self.g.get_card_from_pile("Trade Route")
        self.plr.add_card(self.trade_route, Piles.HAND)

    def test_playZero(self) -> None:
        self.plr.test_input = ["finish selecting"]
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_playOne(self) -> None:
        self.plr.test_input = ["finish selecting"]
        self.g.get_card_from_pile("Estate")
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_playTwo(self) -> None:
        self.plr.test_input = ["finish selecting"]
        self.g.get_card_from_pile("Estate")
        self.g.get_card_from_pile("Province")
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
