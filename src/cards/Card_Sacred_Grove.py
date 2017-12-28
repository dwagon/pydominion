#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_SacredGrove(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.base = 'nocturne'
        self.desc = "+1 Buy; +3 Coin; Receive a Boon. If it doesn't give +1 Coin, each other player may receive it."
        self.name = 'Sacred Grove'
        self.cost = 5
        self.buys = 1
        self.coin = 3

    def special(self, game, player):
        b = player.receive_boon()
        player.output("{} coin={}".format(b.name, b.coin))
        if b.coin == 1:
            return
        for pl in game.playerList():
            if pl == player:
                continue
            ch = pl.plrChooseOptions(
                    "Accept a boon of {} from {}'s Sacred Grove?".format(b.name, player.name),
                    ("Accept ({})".format(b.description(pl)), True),
                    ("Refuse", False)
                )
            if ch:
                pl.receive_boon(b, discard=False)


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    return False    # Don't accept a boon


###############################################################################
class Test_SacredGrove(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Sacred Grove', 'Moat'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Sacred Grove'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_no_share(self):
        """ Play a Sacred Grove with a gift that shouldn't share """
        for b in self.g.boons:
            if b.name == "The Field's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 3 + 1)
            self.assertEqual(self.plr.getBuys(), 1 + 1)
        except AssertionError:
            self.g.print_state()
            raise

    def test_play_share(self):
        """ Play a Sacred Grove with a shared gift """
        for b in self.g.boons[:]:
            if b.name == "The Sea's Gift":
                self.g.boons = [b]
                break
        self.vic.test_input = ['Accept']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 3)
            self.assertEqual(self.plr.getBuys(), 1 + 1)
            self.assertEqual(self.vic.handSize(), 5 + 1)
        except AssertionError:
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
