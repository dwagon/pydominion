#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Farmers_Market"""
import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_FarmersMarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.GATHERING]
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Farmers' Market"
        self.buys = 1
        self.cost = 3

    def desc(self, player):
        """If there are 4VP or more on the Farmers' Market pile, take them and trash this.
        Otherwise, add 1VP to the pile and then +$1 per 1VP on the pile."""
        vps = player.game["Farmers' Market"].getVP()
        if vps >= 4:
            return f"+1 Buy; Take {vps} VPs and trash this."
        return f"+1 Buy; Add 1VP to the pile and then +{vps} Coin."

    def special(self, game, player):
        vps = game["Farmers' Market"].getVP()
        if vps >= 4:
            player.add_score("Farmers' Market", vps)
            player.trash_card(self)
            player.output(f"Gaining {vps} VPs and trashing the Farmers' Market")
            game["Farmers' Market"].drainVP()
        else:
            vps += 1
            player.output(f"Gaining {vps} coins")
            player.coins.add(vps)
            game["Farmers' Market"].addVP()


###############################################################################
class TestFarmersMarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Farmers' Market"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.c1 = self.g["Farmers' Market"].remove()
        self.c2 = self.g["Farmers' Market"].remove()

    def test_play(self):
        """Play a Farmers Market"""
        self.plr.add_actions(2)
        self.plr.add_card(self.c1, Piles.HAND)
        self.g["Farmers' Market"].addVP(3)
        self.plr.play_card(self.c1)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.coins.get(), 4)
        self.plr.add_card(self.c2, Piles.HAND)
        self.plr.play_card(self.c2)
        self.assertEqual(self.plr.get_score_details()["Farmers' Market"], 4)
        self.assertIn("Farmers' Market", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
