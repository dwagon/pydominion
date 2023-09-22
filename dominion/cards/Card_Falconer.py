#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Falconer """

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Falconer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain a card to your hand costing less than this. When any
            player gains a card with 2 or more types (Action, Attack, etc.), you
            may play this from your hand."""
        self.name = "Falconer"
        self.cost = 5

    def special(self, game, player):
        player.plr_gain_card(5)

    def hook_gain_card(self, game, player, card):
        if len(card.get_cardtype_repr().split(",")) >= 2:
            player.output("Falconer lets you gain a card")
            player.plr_gain_card(5)


###############################################################################
class Test_Falconer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Falconer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Falconer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a card"""
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_gaincard(self):
        """Gain a card"""
        self.plr.test_input = ["Get Silver"]
        self.plr.gain_card("Moat")
        self.g.print_state()
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
