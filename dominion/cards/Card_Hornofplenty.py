#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Hornofplenty(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """When you play this, gain a card costing up to 1 per differently named card you have in play, counting this.
        If it's a Victory card, trash this."""
        self.name = "Horn of Plenty"
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for c in player.piles[Piles.PLAYED]:
            cards.add(c.name)

        card = player.plr_gain_card(
            len(cards),
            prompt="Gain a card costing up to %d. If it is a victory then this card will be trashed"
            % len(cards),
        )
        if card and card.isVictory():
            player.trash_card(self)


###############################################################################
class Test_Hornofplenty(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Horn of Plenty", "Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Horn of Plenty")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Horn of Plenty"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Silver")
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Horn of Plenty", self.plr.piles[Piles.PLAYED])

    def test_play_victory(self):
        """Horn of Plenty - gaining a victory card"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Gold", "Moat")
        self.plr.test_input = ["Get Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Horn of Plenty", self.plr.piles[Piles.PLAYED])
        self.assertIn("Horn of Plenty", self.g.trash_pile)

    def test_play_nothing(self):
        """Horn of Plenty - gaining nothing"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Gold", "Moat")
        self.plr.test_input = ["finish selecting"]
        self.plr.play_card(self.card)
        self.assertNotIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Horn of Plenty", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Horn of Plenty", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
