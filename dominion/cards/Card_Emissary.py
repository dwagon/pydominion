#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Emissary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Emissary"
        self.desc = "+3 Cards; If this made you shuffle (at least one card), +1 Action and +2 Favors."
        self.cards = 3
        self.cost = 5

    def hook_post_shuffle(self, game, player):
        player.add_actions(1)
        player.favors.add(2)


###############################################################################
class Test_Emissary(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Emissary"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Emissary"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.deck.set("Copper", "Copper")
        self.plr.discardpile.set("Estate", "Estate", "Estate", "Duchy")
        favs = self.plr.favors.get()
        acts = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), favs + 2)
        self.assertEqual(self.plr.actions.get(), acts - 1 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
