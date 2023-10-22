#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Crossroads(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Reveal your hand. +1 Card per Victory card revealed.
            If this is the first time you played a Crossroads this turn, +3 Actions."""
        self.name = "Crossroads"
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        """Reveal your hand. +1 Card per Victory card revealed.
        If this is the first time you played a Crossroads this turn,
        +3 Actions"""
        vict = 0
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
            if card.isVictory():
                vict += 1
        if vict:
            player.output("Picking up %d cards" % vict)
            player.pickup_cards(vict)
        else:
            player.output("No victory cards")
        numcross = sum([1 for c in player.piles[Piles.PLAYED] if c.name == "Crossroads"])
        if numcross == 1:
            player.add_actions(3)


###############################################################################
class Test_Crossroads(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Crossroads"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Crossroads")

    def test_play(self):
        """Play crossroads once"""
        self.plr.piles[Piles.HAND].set("Silver", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.actions.get(), 3)

    def test_play_twice(self):
        """Play crossroads again"""
        self.plr.piles[Piles.HAND].set("Silver", "Copper", "Crossroads")
        self.plr.piles[Piles.PLAYED].set("Crossroads")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.plr.actions.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
