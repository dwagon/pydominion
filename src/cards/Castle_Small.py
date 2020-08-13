#!/usr/bin/env python

import unittest
import Card
import Game
from cards.Card_Castles import CastleCard


###############################################################################
class Card_SmallCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_VICTORY, Card.TYPE_CASTLE]
        self.base = Game.EMPIRES
        self.cost = 5
        self.desc = "Trash this or a Castle from your hand. If you do, gain a Castle. 2VP"
        self.coin = 1
        self.name = "Small Castle"
        self.victory = 2

    def special(self, game, player):
        cards = [c for c in player.hand if c.isCastle()] + [self]
        tr = player.plrTrashCard(prompt="Trash a Castle to gain another Castle", cardsrc=cards)
        if tr:
            newcast = player.gainCard('Castles')
            player.output("Gained %s" % newcast.name)


###############################################################################
class Test_SmallCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Castles'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Small Castle':
                break

    def test_play(self):
        """ Play a castle - trash nothing"""
        self.plr.test_input = ['Finish']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()['Small Castle'], 2)

    def test_trash(self):
        """ Play a castle - trash self"""
        self.plr.test_input = ['small']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
