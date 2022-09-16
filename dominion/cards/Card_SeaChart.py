#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sea_Chart"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Sea_Chart(Card.Card):
    """Sea Chart"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Card; +1 Action; Reveal the top card of your deck.
            If you have a copy of it in play, put it into your hand."""
        self.name = "Sea Chart"
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """Sea Chart Special"""
        nextcard = player.deck.top_card()
        player.reveal_card(nextcard)
        if nextcard.name in player.played:
            player.output(f"Next card is {nextcard.name}, same as played so moving to hand")
            player.move_card(nextcard, "hand")
        else:
            player.output(f"Next card is {nextcard.name} which hasn't been played")


###############################################################################
class Test_Sea_Chart(unittest.TestCase):
    """Test Sea_Chart"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sea Chart", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sea Chart"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard_match(self):
        """Play a Sea Chart where we have played the same"""
        self.plr.deck.set("Moat", "Copper")
        self.plr.played.set("Moat")
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.hand)

    def test_playcard_nomatch(self):
        """Play a Sea Chart where we haven't played the same"""
        self.plr.deck.set("Moat", "Copper")
        self.plr.played.set("Copper")
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
