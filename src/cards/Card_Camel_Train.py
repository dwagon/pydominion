#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Camel_Train """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Camel_Train(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.MENAGERIE
        self.desc = """Exile a non-Victory card from the Supply. When you gain this, Exile a Gold from the Supply."""
        self.name = 'Camel Train'
        self.cost = 3

    def special(self, game, player):
        cards = [_ for _ in game.cardpiles.values() if not _.isVictory()]
        toex = player.cardSel(prompt="Pick a card to Exile", cardsrc=cards)
        if toex:
            player.exile_card(toex[0].name)

    def hook_gain_this_card(self, game, player):
        player.exile_card('Gold')


###############################################################################
class Test_Camel_Train(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Camel Train'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Camel Train'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.test_input = ['Select Silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_exile('Silver'))

    def test_gain(self):
        self.plr.gainCard('Camel Train')
        self.assertIsNotNone(self.plr.in_exile('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
