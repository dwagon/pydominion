#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Trader(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.REACTION]
        self.base = Game.HINTERLANDS
        self.desc = """Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.
        When you would gain a card, you may reveal this from your hand. If you do, instead, gain a Silver."""
        self.name = 'Trader'
        self.cost = 4

    def special(self, game, player):
        card = player.plrTrashCard(prompt="Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.")
        if card:
            player.output("Gaining %d Silvers" % card[0].cost)
            for _ in range(card[0].cost):
                player.gainCard('Silver')

    def hook_gain_card(self, game, player, card):
        if card.name == 'Silver':
            return {}
        silver = player.plrChooseOptions(
            "From your Trader gain %s or gain a Silver instead?" % card.name,
            ("Still gain %s" % card.name, False),
            ("Instead gain Silver", True))
        if silver:
            return {'replace': 'Silver', 'destination': 'discard'}
        return {}


###############################################################################
class Test_Trader(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Trader'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Trader'].remove()

    def test_play(self):
        """ Play a trader - trashing an estate """
        tsize = self.g.trashSize()
        self.plr.setHand('Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['estate', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discard_size(), 2)
        for i in self.plr.discardpile:
            self.assertEqual(i.name, 'Silver')
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Estate'))

    def test_gain(self):
        self.plr.test_input = ['Instead']
        self.plr.addCard(self.card, 'hand')
        self.plr.setCoin(6)
        self.plr.buyCard(self.g['Gold'])
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertIsNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
