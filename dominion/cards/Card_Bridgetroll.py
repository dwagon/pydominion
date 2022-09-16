#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bridgetroll(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Each other player takes his -1 Coin token.
            Now and at the start of your next turn: +1 Buy.
            While this is in play cards cost 1 less"""
        self.name = "Bridge Troll"
        self.buys = 1
        self.cost = 5
        self._played = False

    def special(self, game, player):
        self._played = True
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Bridge Troll set your -1 Coin token")
            plr.coin_token = True

    def hook_card_cost(self, game, player, card):
        if self._played:
            return -1
        return 0

    def duration(self, game, player):
        self._played = False
        player.buys.add(1)


###############################################################################
class Test_Bridgetroll(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Bridge Troll"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Bridge Troll"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a bridge troll"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertTrue(self.victim.coin_token)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.buys.get(), 2)

    def test_costreduction(self):
        self.coin = 1
        self.assertEqual(self.plr.card_cost(self.g["Gold"]), 6)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.card_cost(self.g["Gold"]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
