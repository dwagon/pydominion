#!/usr/bin/env python

import unittest
from dominion import Card, Game, Player


###############################################################################
class Card_Messenger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Messenger"
        self.buys = 1
        self.coin = 2
        self.cost = 4

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """+1 Buy, +2 Coin, You may put your deck into your discard pile;
                When this is your first buy in a turn, gain a card costing up to 4,
                and each other player gains a copy of it."""
        return "+1 Buy, +2 Coin, You may put your deck into your discard pile"

    def special(self, game, player):
        o = player.plr_choose_options(
            "Put entire deck into discard pile?",
            ("No - keep it as it is", False),
            ("Yes - dump it", True),
        )
        if o:
            for c in player.deck:
                player.add_card(c, "discard")
                player.deck.remove(c)

    def hook_buy_this_card(self, game, player):
        if len(player.stats["bought"]) == 1:
            c = player.plr_gain_card(4, prompt="Pick a card for everyone to gain")
            for plr in game.player_list():
                if plr != player:
                    plr.gain_card(newcard=c)
                    plr.output("Gained a %s from %s's Messenger" % (c.name, player.name))


###############################################################################
class Test_Messenger(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Messenger"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Messenger"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Messenger - do nothing"""
        self.plr.test_input = ["No"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_discard(self):
        """Play a messenger and discard the deck"""
        decksize = self.plr.deck.size()
        self.plr.test_input = ["Yes"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), decksize)

    def test_buy(self):
        """Buy a messenger"""
        self.plr.test_input = ["get silver"]
        self.plr.coins.set(4)
        self.plr.buy_card(self.g["Messenger"])
        for plr in self.g.player_list():
            self.assertIn("Silver", plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
