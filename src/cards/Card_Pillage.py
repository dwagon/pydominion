#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = "Trash this. Each other player with 5 or more cards in hand reveals their hand and discards a card that you choose. Gain 2 Spoils from the Spoils pile."
        self.name = 'Pillage'
        self.required_cards = ['Spoils']
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        player.trashCard(self)
        for plr in player.attackVictims():
            if plr.handSize() < 5:
                player.output("Player %s has too small a hand size" % plr.name)
                continue
            self.pickACard(plr, player)
        for i in range(2):
            player.gainCard('Spoils')

    ###########################################################################
    def pickACard(self, victim, player):
        for card in victim.hand:
            victim.revealCard(card)
        cards = player.cardSel(
            cardsrc=victim.hand,
            prompt="Which card to discard from %s" % victim.name
            )
        card = cards[0]
        victim.discardCard(card)
        victim.output("%s pillaged your %s" % (player.name, card.name))


###############################################################################
class Test_Pillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Pillage'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['Pillage'].remove()

    def test_play(self):
        """ Play the Pillage """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['copper']
        self.victim.setHand('Copper', 'Estate', 'Duchy', 'Gold', 'Silver', 'Province')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Spoils')
        self.assertEqual(self.victim.handSize(), 5)
        self.assertEqual(self.victim.discardSize(), 1)
        self.assertEqual(self.victim.discardpile[0].name, 'Copper')

    def test_short_hand(self):
        """ Play the Pillage with the victim having a small hand"""
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['copper']
        self.victim.setHand('Copper', 'Estate', 'Duchy', 'Gold')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Spoils')
        self.assertEqual(self.victim.handSize(), 4)
        self.assertEqual(self.victim.discardSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
