#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_FarmersMarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'gathering']
        self.base = 'empires'
        self.name = "Farmers' Market"
        self.buys = 1
        self.cost = 3

    def desc(self, player):
        vps = player.game["Farmers' Market"].getVP()
        if vps >= 4:
            return "+1 Buy; Take {} VPs and trash this.".format(vps)
        else:
            return "+1 Buy; Add 1VP to the pile and then +{} Coin.".format(vps)

    def special(self, game, player):
        vps = game["Farmers' Market"].getVP()
        if vps >= 4:
            player.addScore("Farmers' Market", vps)
            player.trashCard(self)
            player.output("Gaining {} VPs and trashing the Farmers' Market".format(vps))
            game["Farmers' Market"].drainVP()
        else:
            vps += 1
            player.output("Gaining {} coins".format(vps))
            player.addCoin(vps)
            game["Farmers' Market"].addVP()


###############################################################################
class Test_FarmersMarket(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Farmers' Market"])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.c1 = self.g["Farmers' Market"].remove()
        self.c2 = self.g["Farmers' Market"].remove()

    def test_play(self):
        """ Play a Farmers Market """
        self.plr.addActions(2)
        self.plr.addCard(self.c1, 'hand')
        self.g["Farmers' Market"].addVP(3)
        self.plr.playCard(self.c1)
        self.assertEqual(self.plr.getBuys(), 1 + 1)
        self.assertEqual(self.plr.getCoin(), 4)
        self.plr.addCard(self.c2, 'hand')
        self.plr.playCard(self.c2)
        self.assertEqual(self.plr.getScoreDetails()["Farmers' Market"], 4)
        self.assertIsNotNone(self.g.inTrash("Farmers' Market"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
