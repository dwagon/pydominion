#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Zombie_Mason(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ZOMBIE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Trash the top card of your deck. You may gain a card costing up to 1 more than it."
        self.name = "Zombie Mason"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game):
        game.trash_pile.add(self)

    def special(self, game, player):
        topdeck = player.top_card()
        player.trash_card(topdeck)
        player.output(f"Trashed {topdeck.name} from the top of your deck")
        player.plr_gain_card(topdeck.cost + 1)


###############################################################################
class Test_Zombie_Mason(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Zombie Mason", "Guide"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Zombie Mason")

    def test_play(self):
        self.plr.piles[Piles.DECK].set("Estate")
        self.plr.test_input = ["Guide"]
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertIn("Guide", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
