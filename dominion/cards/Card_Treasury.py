#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Treasury(Card.Card):
    """Treasury"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Card +1 Action +1 Coin; When you discard this from play,
            if you didn't buy a Victory card this turn, you may put this on top
            of your deck."""
        self.name = "Treasury"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.coin = 1

    def hook_discard_this_card(self, game, player, source):
        vict = False
        for card in player.stats["bought"]:
            if card.isVictory():
                vict = True
        if vict:
            topdeck = player.plr_choose_options(
                "Put Treasury back on top of your deck?",
                ("Discard as normal", False),
                ("Put on top of your deck", True),
            )
            if topdeck:
                player.move_card(self, "topdeck")


###############################################################################
class TestTreasury(unittest.TestCase):
    """Test Treasury"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Treasury"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Treasury")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a trader - trashing an estate"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy_top_deck(self):
        self.plr.test_input = ["put on top"]
        self.plr.coins.set(5)
        self.plr.buy_card("Duchy")
        self.plr.discard_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Treasury")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
