#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Herald"""

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Herald(Card.Card):
    """Herald"""

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
        """Variable description"""
        if player.phase == Player.Phase.BUY:
            return """+1 Card +1 Action. Reveal the top card of your deck.
                If it is an Action, play it.  When you buy this, you may overpay
                for it. For each Coin you overpaid, look through your discard pile
                and put a card from it on top of your deck."""
        return "+1 Card +1 Action. Reveal the top card of your deck. If it is an Action, play it."

    def special(self, game, player):
        card = player.top_card()
        player.reveal_card(card)
        if card.isAction():
            player.move_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)

    def hook_overpay(self, game, player, amount):  # pylint: disable=unused-argument
        """If we overpay"""
        for _ in range(amount):
            card = player.card_sel(
                num=1,
                force=True,
                cardsrc="discard",
                prompt="Look through your discard pile and put a card from it on top of your deck",
            )
            if card:
                player.add_card(card[0], "topdeck")
                player.piles[Piles.DISCARD].remove(card[0])


###############################################################################
class TestHerald(unittest.TestCase):
    """Test Herald"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Herald", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Herald"].remove()

    def test_play_action(self):
        """Play a Herald  - action top card"""
        self.plr.piles[Piles.DECK].set("Province", "Estate", "Copper", "Moat", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), 5 + 1 + 2
        )  # 5 for hand, 1 for herald, 2 for moat
        self.assertEqual(self.plr.actions.get(), 1 + 1)
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])

    def test_play_non_action(self):
        """Play a Herald - non-action top card"""
        self.plr.piles[Piles.DECK].set("Gold", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 1 + 1)
        self.assertIn("Gold", self.plr.piles[Piles.DECK])

    def test_buy(self):
        """Buy a Herald"""
        self.plr.coins.set(5)
        self.plr.test_input = ["1", "moat"]
        self.plr.piles[Piles.DISCARD].set("Estate", "Moat", "Copper")
        self.plr.buy_card(self.g["Herald"])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Moat")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
