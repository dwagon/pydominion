#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Survivors """

import unittest
import Game
import Card


###############################################################################
class Card_Survivors(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.purchasable = False
        self.cost = 0
        self.desc = "Look at the top 2 cards of your deck. Discard them or put them back in any order."
        self.name = "Survivors"

    def special(self, game, player):
        """ Look at the top 2 cards of your deck. Discard them or
            put them back in any order """
        crds = player.pickupCards(2)
        ans = player.plrChooseOptions(
            "What to do with survivors?",
            ("Discard {} and {}".format(crds[0].name, crds[1].name), 'discard'),
            ("Return {} and {} to deck".format(crds[0].name, crds[1].name), 'return')
        )
        if ans == 'discard':
            player.discardCard(crds[0])
            player.discardCard(crds[1])
        else:
            player.addCard(crds[0], 'deck')
            player.addCard(crds[1], 'deck')


###############################################################################
class Test_Survivors(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=4, initcards=['Cultist'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Ruins'].remove()
            if self.card.name == 'Survivors':
                break
        self.plr.addCard(self.card, 'hand')

    def test_play_discard(self):
        """ Play a survivor and discard cards """
        self.plr.setDeck('Copper', 'Silver', 'Gold')
        self.plr.test_input = ['Discard']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertIsNone(self.plr.in_hand('Gold'))
        self.assertIsNone(self.plr.in_hand('Silver'))

    def test_play_keep(self):
        """ Play a survivor and keep cards """
        self.plr.setDeck('Copper', 'Silver', 'Gold')
        self.plr.test_input = ['Return']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_discard('Gold'))
        self.assertIsNone(self.plr.in_discard('Silver'))
        self.assertIsNotNone(self.plr.in_hand('Gold'))
        self.assertIsNotNone(self.plr.in_hand('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
