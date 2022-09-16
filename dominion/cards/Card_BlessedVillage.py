#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_BlessedVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Blessed Village"
        self.actions = 2
        self.cards = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            return "+1 Card; +2 Actions; When you gain this, take a Boon. Receive it now or at the start of your next turn."
        return "+1 Card; +2 Actions"

    def hook_gain_this_card(self, game, player):
        player.receive_boon()


###############################################################################
class Test_BlessedVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Blessed Village"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Blessed Village"].remove()
        for b in self.g.boons:
            if b.name == "The Sea's Gift":
                myboon = b
                break
        self.g.boons = [myboon]

    def test_play_card(self):
        """Play Blessed Village"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_gain(self):
        self.plr.gain_card("Blessed Village")
        self.assertEqual(self.plr.hand.size(), 5 + 1)  # 1 from boon


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
