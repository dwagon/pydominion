#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_SacredGrove(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Buy; +3 Coin; Receive a Boon. If it doesn't give +1 Coin, each other player may receive it."
        self.name = "Sacred Grove"
        self.cost = 5
        self.buys = 1
        self.coin = 3

    def special(self, game, player):
        b = player.receive_boon()
        player.output(f"{b.name} coin={b.coin}")
        if b.coin == 1:
            return
        for pl in game.player_list():
            if pl == player:
                continue
            ch = pl.plr_choose_options(
                f"Accept a boon of {b.name} from {player.name}'s Sacred Grove?",
                (f"Accept ({b.description(pl)})", True),
                ("Refuse", False),
            )
            if ch:
                pl.receive_boon(b, discard=False)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return False  # Don't accept a boon


###############################################################################
class Test_SacredGrove(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Sacred Grove", "Moat"],
            badcards=["Druid"],
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Sacred Grove")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_no_share(self):
        """Play a Sacred Grove with a gift that shouldn't share"""
        for b in self.g.boons:
            if b.name == "The Field's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 3 + 1)
            self.assertEqual(self.plr.buys.get(), 1 + 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_play_share(self):
        """Play a Sacred Grove with a shared gift"""
        for b in self.g.boons[:]:
            if b.name == "The Sea's Gift":
                self.g.boons = [b]
                break
        self.vic.test_input = ["Accept"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 3)
            self.assertEqual(self.plr.buys.get(), 1 + 1)
            self.assertEqual(self.vic.piles[Piles.HAND].size(), 5 + 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
