#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_BridgeTroll(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Each other player takes their –$1 token.
            On this turn and your next turn, cards cost $1 less.
            Now and at the start of your next turn: +1 Buy."""
        self.name = "Bridge Troll"
        self.buys = 1
        self.cost = 5
        self._played = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        self._played = True
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Bridge Troll set your -1 Coin token")
            plr.coin_token = True

    def hook_card_cost(self, game: Game.Game, player: Player.Player, card: Card.Card) -> int:
        if self._played:
            return -1
        return 0

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        self._played = False
        player.buys.add(1)
        return {}


###############################################################################
class TestBridgeTroll(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Bridge Troll"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Bridge Troll")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a bridge troll"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertTrue(self.victim.coin_token)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.buys.get(), 2)

    def test_cost_reduction(self) -> None:
        self.coin = 1
        gold = self.g.get_card_from_pile("Gold")
        self.assertEqual(self.plr.card_cost(gold), 6)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.card_cost(gold), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
