#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Royalseal(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+2 coin. Cards gain go to top of deck"
        self.playable = False
        self.name = 'Royal Seal'
        self.cost = 5
        self.coin = 2

    def hook_gainCard(self, game, player, card):
        """ While this is in play, when you gain a card, you may
            put that card on top of your deck"""
        mod = {}
        deck = player.plrChooseOptions(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True))
        if deck:
            player.output("Putting %s on deck due to Royal Seal" % card.name)
            mod['destination'] = 'topdeck'
        return mod


###############################################################################
class Test_Royalseal(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Royal Seal'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Royal Seal'].remove()

    def test_play(self):
        """ Play a Royal Seal """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_discard(self):
        """ Have a Royal Seal  - discard the gained card"""
        self.plr.setPlayed('Royal Seal')
        self.plr.test_input = ['discard']
        self.plr.gainCard('Gold')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Gold')
        self.assertFalse(self.plr.inHand('Gold'))

    def test_deck(self):
        """ Have a Royal Seal  - the gained card on the deck"""
        self.plr.setPlayed('Royal Seal')
        self.plr.test_input = ['deck']
        self.plr.gainCard('Gold')
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertIsNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
