#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_FarmersMarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_GATHERING]
        self.base = Game.EMPIRES
        self.name = "Farmers' Market"
        self.buys = 1
        self.cost = 3

    def desc(self, player):
        vps = player.game["Farmers' Market"].getVP()
        if vps >= 4:
            return "+1 Buy; Take {} VPs and trash this.".format(vps)
        return "+1 Buy; Add 1VP to the pile and then +{} Coin.".format(vps)

    def special(self, game, player):
        vps = game["Farmers' Market"].getVP()
        if vps >= 4:
            player.add_score("Farmers' Market", vps)
            player.trash_card(self)
            player.output("Gaining {} VPs and trashing the Farmers' Market".format(vps))
            game["Farmers' Market"].drainVP()
        else:
            vps += 1
            player.output("Gaining {} coins".format(vps))
            player.add_coins(vps)
            game["Farmers' Market"].addVP()


###############################################################################
class Test_FarmersMarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Farmers' Market"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.c1 = self.g["Farmers' Market"].remove()
        self.c2 = self.g["Farmers' Market"].remove()

    def test_play(self):
        """Play a Farmers Market"""
        self.plr.add_actions(2)
        self.plr.add_card(self.c1, "hand")
        self.g["Farmers' Market"].addVP(3)
        self.plr.play_card(self.c1)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.get_coins(), 4)
        self.plr.add_card(self.c2, "hand")
        self.plr.play_card(self.c2)
        self.assertEqual(self.plr.get_score_details()["Farmers' Market"], 4)
        self.assertIsNotNone(self.g.in_trash("Farmers' Market"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
