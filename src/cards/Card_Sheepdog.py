#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sheepdog """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Sheepdog(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.REACTION]
        self.base = Game.MENAGERIE
        self.desc = "+2 Cards; When you gain a card, you may play this from your hand."
        self.name = 'Sheepdog'
        self.cards = 2
        self.cost = 3

    def hook_gain_card(self, game, player, card):
        player.playCard(self, costAction=False)


###############################################################################
class Test_Sheepdog(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Sheepdog'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Sheepdog'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play card """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 2)

    def test_gain(self):
        """ Gain a card """
        self.plr.gainCard('Estate')
        self.g.print_state()
        self.assertEqual(self.plr.handSize(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
