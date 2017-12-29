#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Exorcist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night']
        self.base = 'nocturne'
        self.desc = "Trash a card from your hand. Gain a cheaper Spirit from one of the Spirit piles."
        self.name = 'Exorcist'
        self.cost = 4
        self.required_cards = [('Card', 'Ghost'), ('Card', 'Imp'), ('Card', "Will-o'-Wisp")]

    def special(self, game, player):
        card = player.plrTrashCard(prompt="Trash a card and gain a cheaper spirit")
        cost = card[0].cost
        player.plrGainCard(cost=cost, types={'spirit': True}, prompt="Gain a spirit costing up to {}".format(cost))


###############################################################################
class Test_Exorcist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Exorcist'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Exorcist'].remove()

    def test_play(self):
        self.plr.setHand('Silver', 'Gold', 'Province')
        self.plr.test_input = ['Silver']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
