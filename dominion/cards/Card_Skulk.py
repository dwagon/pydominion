#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Skulk(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Skulk"
        self.buys = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "+1 Buy; Each other player receives the next Hex; When you gain this, gain a Gold."
        return "+1 Buy; Each other player receives the next Hex."

    def hook_gain_this_card(self, game, player):
        player.gain_card("Gold")

    def special(self, game, player):
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Skulk hexed you")
            plr.receive_hex()


###############################################################################
class Test_Skulk(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Skulk"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.Skulk = self.g.get_card_from_pile("Skulk")
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_card(self):
        """Play Skulk"""
        self.plr.add_card(self.Skulk, Piles.HAND)
        self.plr.play_card(self.Skulk)
        self.assertTrue(self.vic.has_state("Deluded"))

    def test_gain(self):
        self.plr.gain_card("Skulk")
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
