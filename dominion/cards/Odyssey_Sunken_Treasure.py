#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sunken_Treasure"""

import unittest
from dominion import Game, Card


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
        acts = [
            _ for _ in game.cardTypes() if _.isAction() and _.name not in player.played
        ]
        card = player.card_sel(cardsrc=acts, prompt="Gain a card")
        player.gain_card(card[0])


###############################################################################
class Test_Sunken_Treasure(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys", "Moat", "Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Odysseys"].remove()
            if card.name == "Sunken Treasure":
                break
        self.card = card

    def test_play(self):
        """Play the card"""
        self.plr.played.set("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Militia"]
        self.plr.play_card(self.card)
        self.assertIn("Militia", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
