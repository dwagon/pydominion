#!/usr/bin/env python

import unittest
from dominion import Card, Game, Player


###############################################################################
class Card_Herald(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.GUILDS
        self.name = "Herald"
        self.overpay = True
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """+1 Card +1 Action. Reveal the top card of your deck.
                If it is an Action, play it.  When you buy this, you may overpay
                for it. For each Coin you overpaid, look through your discard pile
                and put a card from it on top of your deck."""
        return "+1 Card +1 Action. Reveal the top card of your deck. If it is an Action, play it."

    def special(self, game, player):
        card = player.next_card()
        player.reveal_card(card)
        if card.isAction():
            player.add_card(card, "hand")
            player.play_card(card, costAction=False)

    def hook_overpay(self, game, player, amount):
        for _ in range(amount):
            card = player.card_sel(
                num=1,
                force=True,
                cardsrc="discard",
                prompt="Look through your discard pile and put a card from it on top of your deck",
            )
            player.add_card(card[0], "topdeck")
            player.discardpile.remove(card[0])


###############################################################################
class Test_Herald(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Herald", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Herald"].remove()

    def test_play(self):
        """Play a Herald"""
        self.plr.deck.set("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.actions.get(), 1 + 1)
        self.assertIn("Moat", self.plr.played)

    def test_buy(self):
        """Buy a Herald"""
        self.plr.coins.set(5)
        self.plr.test_input = ["1", "moat"]
        self.plr.discardpile.set("Estate", "Moat", "Copper")
        self.plr.buy_card(self.g["Herald"])
        self.assertEqual(self.plr.deck[-1].name, "Moat")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
