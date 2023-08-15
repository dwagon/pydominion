#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Monkey """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Monkey(Card.Card):
    """Monkey"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Until your next turn, when the player to your right gains a card,
            +1 Card.  At the start of your next turn, +1 Card."""
        self.name = "Monkey"
        self.cost = 3

    def hook_allplayers_gain_card(self, game, player, owner, card):
        """Until your next turn, when the player to your right gains a card, +1 Card"""
        if player == game.playerToRight(owner):
            owner.pickup_card()

    def duration(self, game, player):
        """At the start of your next turn, +1 Card."""
        player.pickup_card()


###############################################################################
class Test_Monkey(unittest.TestCase):
    """Test Monkey"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Monkey", "Moat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Monkey"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play Monkey"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.oth.gain_card("Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
