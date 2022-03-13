#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Minion(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.INTRIGUE
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
        attack = player.plrChooseOptions(
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
            player.addCoin(2)

    def attack(self, game, player):
        self.dropAndDraw(player)
        for victim in player.attackVictims():
            if victim.hand.size() >= 5:
                self.dropAndDraw(victim)

    def dropAndDraw(self, plr):
        # TODO: Do you discard the minion as well?
        plr.discardHand()
        plr.pickupCards(4)


###############################################################################
class Test_Minion(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Minion", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Minion"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play_gold(self):
        """Play a minion and gain two gold"""
        self.plr.test_input = ["0"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5)

    def test_play_discard(self):
        """Play a minion and discard hand"""
        self.plr.test_input = ["1"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.discardpile.size(), 5 + 1)
        self.assertEqual(self.victim.hand.size(), 4)
        self.assertEqual(self.victim.discardpile.size(), 5)

    def test_play_victim_smallhand(self):
        """Play a minion and discard hand - the other player has a small hand"""
        self.victim.set_hand("Estate", "Estate", "Estate", "Estate")
        self.plr.test_input = ["1"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.discardpile.size(), 5 + 1)
        self.assertEqual(self.victim.hand.size(), 4)
        self.assertEqual(self.victim.discardpile.size(), 0)

    def test_play_defended(self):
        """Play a minion and discard hand - the other player is defended"""
        self.victim.set_hand("Estate", "Estate", "Estate", "Estate", "Moat")
        self.plr.test_input = ["1"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(self.plr.discardpile.size(), 5 + 1)
        self.assertEqual(self.victim.hand.size(), 5)
        self.assertEqual(self.victim.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
