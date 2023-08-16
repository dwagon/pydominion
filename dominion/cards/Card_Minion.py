#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Minion(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+1 Action; Choose one: +2 Coin; or discard your hand,
            +4 Cards, and each other player with at least 5 cards in hand discards
            his hand and draws 4 cards."""
        self.name = "Minion"
        self.cost = 5
        self.actions = 1

    def special(self, game, player):
        """Choose one: +2 coin or
        discard your hand, +4 cards and each other player with
        at least 5 card in hand discards his hand and draws 4
        cards"""
        attack = player.plr_choose_options(
            "What do you want to do?",
            ("+2 coin", False),
            (
                "Discard your hand, +4 cards and each other player with 5 cards discards and draws 4",
                True,
            ),
        )
        if attack:
            self.attack(game, player)
        else:
            player.coins.add(2)

    def attack(self, game, player):
        self.dropAndDraw(player)
        for victim in player.attack_victims():
            if victim.piles[Piles.HAND].size() >= 5:
                self.dropAndDraw(victim)

    def dropAndDraw(self, plr):
        # TODO: Do you discard the minion as well?
        plr.discard_hand()
        plr.pickup_cards(4)


###############################################################################
class Test_Minion(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Minion", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Minion"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_gold(self):
        """Play a minion and gain two gold"""
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_play_discard(self):
        """Play a minion and discard hand"""
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5 + 1)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 4)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 5)

    def test_play_victim_smallhand(self):
        """Play a minion and discard hand - the other player has a small hand"""
        self.victim.piles[Piles.HAND].set("Estate", "Estate", "Estate", "Estate")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5 + 1)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 4)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 0)

    def test_play_defended(self):
        """Play a minion and discard hand - the other player is defended"""
        self.victim.piles[Piles.HAND].set("Estate", "Estate", "Estate", "Estate", "Moat")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5 + 1)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
