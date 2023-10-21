#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Enlarge"""
import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Enlarge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Now and at the start of your next turn: Trash a card from your hand,
        and gain one costing up to $2 more."""
        self.name = "Enlarge"
        self.cost = 5

    def special(self, game, player):
        self.effect(player)

    def duration(self, game, player):
        self.effect(player)

    def effect(self, player):
        if trash := player.plr_trash_card(force=True):
            cost = player.card_cost(trash[0]) + 2
            player.plr_gain_card(cost)


###############################################################################
class TestEnlarge(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Enlarge"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Enlarge")

    def test_play(self):
        """Play a Enlarge"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Silver", "Get Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.g.trash_pile)
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.end_turn()
        self.plr.test_input = ["Trash Gold", "Get Province"]
        self.plr.start_turn()
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
