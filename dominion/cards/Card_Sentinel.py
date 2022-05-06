#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sentinel"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Sentinel(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALLIES
        self.name = "Sentinel"
        self.desc = "Look at the top 5 cards of your deck. You may trash up to 2 of them. Put the rest back in any order."
        self.cost = 3

    def special(self, game, player):
        cards = []
        for _ in range(5):
            cards.append(player.next_card())
        player.output("Trash up to 2 of these")
        trashed = player.plr_trash_card(num=2, cardsrc=cards)
        for card in cards:
            if card not in trashed:
                player.add_card(card, "topdeck")


###############################################################################
class Test_Sentinel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sentinel"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Sentinel"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.deck.set("Province", "Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Trash Copper", "Finish"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIn("Silver", self.plr.deck)
        self.assertIn("Gold", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
