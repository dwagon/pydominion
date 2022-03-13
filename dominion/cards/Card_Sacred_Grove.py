#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_SacredGrove(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = Game.NOCTURNE
        self.desc = "+1 Buy; +3 Coin; Receive a Boon. If it doesn't give +1 Coin, each other player may receive it."
        self.name = "Sacred Grove"
        self.cost = 5
        self.buys = 1
        self.coin = 3

    def special(self, game, player):
        b = player.receive_boon()
        player.output("{} coin={}".format(b.name, b.coin))
        if b.coin == 1:
            return
        for pl in game.player_list():
            if pl == player:
                continue
            ch = pl.plrChooseOptions(
                "Accept a boon of {} from {}'s Sacred Grove?".format(
                    b.name, player.name
                ),
                ("Accept ({})".format(b.description(pl)), True),
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
        self.g = Game.Game(
            quiet=True,
            numplayers=2,
            initcards=["Sacred Grove", "Moat"],
            badcards=["Druid"],
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Sacred Grove"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_no_share(self):
        """Play a Sacred Grove with a gift that shouldn't share"""
        for b in self.g.boons:
            if b.name == "The Field's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 3 + 1)
            self.assertEqual(self.plr.get_buys(), 1 + 1)
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
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 3)
            self.assertEqual(self.plr.get_buys(), 1 + 1)
            self.assertEqual(self.vic.hand.size(), 5 + 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
