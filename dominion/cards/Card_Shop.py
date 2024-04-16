#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Shop(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.desc = (
            """+1 Card, +1 Coin. You may play an Action card from your hand that you don't have a copy of in play."""
        )
        self.name = "Shop"
        self.cards = 1
        self.coin = 1
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction() and _.name not in player.piles[Piles.PLAYED]]
        if not actions:
            return
        options = [("Play nothing", None)]
        for card in actions:
            options.append((f"Play {card}", card))
        if to_play := player.plr_choose_options("What action do you want to play?", *options):
            player.play_card(to_play, cost_action=False)


###############################################################################
class Test_Shop(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Shop", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Shop")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.PLAYED)
        coins = self.plr.coins.get()
        num_cards = self.plr.piles[Piles.HAND].size()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), num_cards + 1 - 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)

    def test_play_with_action(self) -> None:
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play Moat"]
        num_cards = self.plr.piles[Piles.HAND].size()
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), num_cards + 1 - 1 + 2 - 1
        )  # +1 for shop, -1 for playing shop, -1 for playing moat, +2 for moat effects


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
