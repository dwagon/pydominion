#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Smugglers(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """Gain a copy of a card costing up to 6 that the player to your right gained on his last turn."""
        self.name = "Smugglers"
        self.cost = 3

    def special(self, game, player):
        plr = game.playerToRight(player)
        cards = [_ for _ in plr.stats["bought"] if _.cost <= 6]
        if cards:
            card = player.card_sel(cardsrc=cards)
            if card:
                game[card[0]].remove()
                player.add_card(card[0])
        else:
            player.output(f"{plr.name} didn't buy any suitable cards")


###############################################################################
class Test_Smugglers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Smugglers"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Smugglers"].remove()

    def test_play(self):
        """Play a smugglers"""
        self.other.stats["bought"] = [self.g["Gold"].remove()]
        self.plr.test_input = ["gold"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
