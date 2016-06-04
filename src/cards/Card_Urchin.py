#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Urchin(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = """+1 Card +1 Action
        Each other player discards down to 4 cards in hand.
        When you play another Attack card with this in play, you may trash this.
        If you do, gain a Mercenary from the Mercenary pile."""
        self.name = 'Urchin'
        self.needsmercenary = True
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.output("Discard down to 4 cards from %s's Urchin" % player.name)
            plr.plrDiscardDownTo(4)

    def hook_endTurn(self, game, player):
        attacks = 0
        for card in player.played:
            if card.isAttack():
                attacks += 1
        # Urchin and one more
        if attacks >= 2:
            trash = player.plrChooseOptions(
                "Trash the urchin?",
                ("Keep the Urchin", False),
                ("Trash and gain a Mercenary", True)
                )
            if trash:
                player.trashCard(self)
                player.gainCard("Mercenary")


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):
    numtodiscard = len(player.hand) - 4
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Urchin(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Urchin', 'Militia'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['Urchin'].remove()

    def test_play(self):
        """ Play an Urchin """
        self.plr.addCard(self.card, 'hand')
        self.victim.test_input = ['1', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.victim.handSize(), 4)

    def test_merc(self):
        """ Play an Urchin and get a mercenary """
        self.plr.setPlayed('Urchin', 'Militia')
        self.plr.test_input = ['end phase', 'end phase', 'mercenary']
        self.plr.turn()
        self.g.print_state()
        self.assertIsNotNone(self.plr.inDiscard('Mercenary'))
        self.assertIsNone(self.plr.inHand('Urchin'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
