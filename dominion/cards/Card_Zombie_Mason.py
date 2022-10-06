#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Zombie_Mason(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ZOMBIE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "Trash the top card of your deck. You may gain a card costing up to 1 more than it."
        )
        self.name = "Zombie Mason"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game):
        game.trashpile.add(self)

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
        self.plr = self.g.player_list(0)
        self.card = self.g["Zombie Mason"].remove()

    def test_play(self):
        self.plr.deck.set("Estate")
        self.plr.test_input = ["Guide"]
        self.plr.play_card(self.card, discard=False, costAction=False)
        self.assertIn("Estate", self.g.trashpile)
        self.assertIn("Guide", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
