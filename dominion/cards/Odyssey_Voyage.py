#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Voyage"""

import unittest
from dominion import Game, Card


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
        self._taketurn = False

    def special(self, game, player):
        if game.last_turn(player):
            self._taketurn = True
        else:
            player.output("You had the previous turn")

    def hook_end_turn(self, game, player):
        if self._taketurn:
            player.output("Having a second turn due to Voyage")
            player.playlimit = 3
            self._taketurn = False
            game.current_player = game.playerToRight(player)


###############################################################################
class Test_Voyage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Odysseys"].remove()
            if card.name == "Voyage":
                break
        self.card = card

    def test_play(self):
        """Play the card"""
        self.plr.hand.set("Estate", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        # TODO - testing


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
