#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Mining_Road"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_MiningRoad(Card.Card):
    """Mining Road"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Action; +1 Buy; +$2; Once this turn, when you gain a Treasure, you may play it."""
        self.coin = 2
        self.actions = 1
        self.buys = 1
        self.name = "Mining Road"
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        """Once this turn, when you gain a Treasure, you may play it."""
        if not card.isTreasure():
            return
        if not player.do_once("Mining Road"):
            return
        player.play_card(card, cost_action=False, discard=False)


###############################################################################
class Test_MiningRoad(unittest.TestCase):
    """Test Mining Road"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mining Road"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mining Road")

    def test_play(self):
        """Play a card"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        actions = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)

    def test_gain(self):
        """Gain a treasure"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        coins = self.plr.coins.get()
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.coins.get(), coins + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
