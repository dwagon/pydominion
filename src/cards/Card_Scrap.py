#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Scrap """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Scrap(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'menagerie'
        self.desc = """Trash a card from your hand.
            Choose a different thing per coin it costs: +1 Card; +1 Action; +1 Buy;
            +1 Coin; gain a Silver; gain a Horse."""
        self.name = 'Scrap'
        self.cost = 3
        self.required_cards = [('Card', 'Horse')]

    def special(self, game, player):
        trc = player.plrTrashCard(
            printcost=True,
            prompt="Trash a card from your hand for benefits"
        )
        if not trc:
            return
        cost = player.cardCost(trc[0])
        if cost >= 1:
            player.pickupCard()
        if cost >= 2:
            player.addActions(1)
        if cost >= 3:
            player.addBuys(1)
        if cost >= 4:
            player.addCoin(1)
        if cost >= 5:
            player.gainCard('Silver')
            player.output("Gained a Silver")
        if cost >= 6:
            player.gainCard('Horse')
            player.output("Gained a Horse")


###############################################################################
class Test_Scrap(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Scrap'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Scrap'].remove()

    def test_playcard_cost0(self):
        """ Play a scrap and trash something worth 0 """
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash copper']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Copper'))

    def test_playcard_cost3(self):
        """ Play a scrap and trash something worth 3 """
        self.plr.setHand('Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Province')
        self.plr.test_input = ['trash silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Silver'))
        self.assertIsNotNone(self.plr.inHand('Province'))
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getActions(), 1)

    def test_playcard_cost6(self):
        """ Play a scrap and trash something worth more than 6 """
        self.plr.setHand('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Copper')
        self.plr.test_input = ['trash province']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Province'))
        self.assertIsNotNone(self.plr.inHand('Copper'))
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertIsNotNone(self.plr.in_discard('Horse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
