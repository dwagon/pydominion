#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hostelry """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Hostelry(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'menagerie'
        self.name = 'Hostelry'
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.required_cards = [('Card', 'Horse')]

    def desc(self, player):
        if player.phase == "buy":
            return "+1 Card; +2 Actions; When you gain this, you may discard any number of Treasures, revealed, to gain that many Horses."
        return "+1 Card; +2 Actions"

    def hook_gain_this_card(self, game, player):
        treas = [_ for _ in player.hand if _.isTreasure()]
        if not treas:
            player.output("No suitable cards for Hostelry")
            return
        discards = player.cardSel(
            prompt="Discard number of cards to gain that number of horses",
            verbs=('Discard', 'Undiscard'),
            anynum=True,
            cardsrc=treas
            )
        for crd in discards:
            player.discardCard(crd)
            player.revealCard(crd)
            player.gainCard('Horse')


###############################################################################
class Test_Hostelry(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hostelry'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Hostelry'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a card """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getActions(), 2)

    def test_gain(self):
        """ Gain the card """
        self.plr.setHand('Copper', 'Silver', 'Gold')
        self.plr.test_input = ['Copper', 'Silver', 'Finish']
        self.plr.gainCard('Hostelry')
        self.assertIsNotNone(self.plr.inDiscard('Horse'))
        self.assertIsNone(self.plr.inHand('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
