#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Territory """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Territory(Card.Card):
    """Territory"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.VICTORY,
            Card.CardType.CLASH,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.name = "Territory"
        self.desc = """Worth 1VP per differently named Victory card you have.
            When you gain this, gain a Gold per empty Supply pile."""

    def hook_gain_this_card(self, game, player):
        """When you gain this, gain a Gold per empty Supply pile."""
        empties = sum(
            1 for st, _ in game.get_card_piles() if game.card_piles[st].is_empty()
        )
        for _ in range(empties):
            player.gain_card("Gold")

    def special_score(self, game, player):
        """Worth 1VP per differently named Victory card you have."""
        vict = {_.name for _ in player.all_cards() if _.isVictory()}
        return len(vict)


###############################################################################
class TestTerritory(unittest.TestCase):
    """Test Territory"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Clashes"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Play a Territory"""
        while True:
            card = self.g.get_card_from_pile("Clashes")
            if card.name == "Territory":
                break
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Duchy")
        # Empty Duchy Pile
        c = self.g.get_card_from_pile("Duchy")
        while c:
            c = self.g.get_card_from_pile("Duchy")
        self.plr.gain_card("Clashes")
        score = self.plr.get_score_details()
        self.assertEqual(score["Territory"], 3)  # Estate, Duchy, Territory
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
