#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sunken_Treasure"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Sunken_Treasure(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.ODYSSEY]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.name = "Sunken Treasure"
        self.desc = """Gain an Action card you don't have a copy of in play."""

    def special(self, game, player):
        options = []
        for name, pile in game.card_piles():
            card = game.get_card_from_pile(name)
            if not card.isAction():
                continue
            if name in player.piles[Piles.PLAYED]:
                continue
            options.append((f"Gain {name}", name))
        to_gain = player.plr_choose_options("Gain a card", *options)
        player.gain_card(to_gain)


###############################################################################
class TestSunkenTreasure(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys", "Moat", "Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Odysseys", "Sunken Treasure")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.PLAYED].set("Moat", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gain Militia"]
        self.plr.play_card(self.card)
        self.assertIn("Militia", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
