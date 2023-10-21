#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Voyage"""

import unittest
from dominion import Game, Card, Piles, Limits


###############################################################################
class Card_Voyage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ODYSSEY,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.actions = 1
        self.name = "Voyage"
        self.desc = """+1 Action; If the previous turn wasn't yours, take an
            extra turn after this one, during which you can only play 3 cards
            from your hand."""
        self._take_turn = False
        self.pile = "Odysseys"

    def special(self, game, player):
        if game.last_turn(player):
            self._take_turn = True
        else:
            player.output("You had the previous turn")

    def hook_end_turn(self, game, player):
        if self._take_turn:
            player.output("Having a second turn due to Voyage")
            player.limits[Limits.PLAY] = 3
            self._take_turn = False
            game.current_player = game.playerToRight(player)


###############################################################################
class TestVoyage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Odysseys", "Voyage")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        # TODO - testing


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
