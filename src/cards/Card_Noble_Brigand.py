#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Noble_Brigand(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'hinterlands'
        self.desc = """+1 Coin. When you buy this or play it, each other player reveals
        the top 2 cards of his deck, trashes a revealed Silver or Gold you choose,
        and discards the rest. If he didn't reveal a Treasure, he gains a Copper. You gain the trashed cards."""
        self.name = 'Noble Brigand'
        self.coin = 1
        self.cost = 4

    def special(self, game, player):
        self.attack(game, player)

    def hook_buyThisCard(self, game, player):
        self.attack(game, player)

    def attack(self, game, player):
        for victim in player.attackVictims():
            cards = self.getTreasureCards(victim, player)
            if not cards:
                victim.output("%s's Noble Brigand gave you a copper" % player.name)
                victim.gainCard('Copper')
                return
            ans = None
            choices = []
            for card in cards:
                if card.name in ('Silver', 'Gold'):
                    choices.append(("Steal %s" % card.name, card))
            if choices:
                ans = player.plrChooseOptions("Pick a card to steal", *choices)
            for card in cards:
                if card == ans:
                    victim.output("%s's Noble Brigand stole your %s" % (player.name, card.name))
                    player.output("Stole %s from %s" % (card.name, victim.name))
                    player.addCard(ans)
                else:
                    victim.output("%s's Noble Brigand discarded your %s" % (player.name, card.name))
                    victim.discardCard(card)

    def getTreasureCards(self, plr, player):
        cards = []
        for i in range(2):
            c = plr.nextCard()
            plr.revealCard(c)
            if c.isTreasure():
                cards.append(c)
            else:
                plr.output("%s's Noble Brigand discarded your %s" % (player.name, c.name))
                plr.addCard(c, 'discard')
        return cards


###############################################################################
class Test_Noble_Brigand(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Noble Brigand'])
        self.g.start_game()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Noble Brigand'].remove()

    def test_play(self):
        """ Play an Noble Brigand but without anything to steal"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_no_treasure(self):
        """ Play an Noble Brigand but with no treasure"""
        self.vic.setDeck('Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.vic.discardSize(), 3)
        self.assertIsNotNone(self.vic.inDiscard('Copper'))

    def test_gold(self):
        """ Play an Noble Brigand with a gold """
        self.vic.setDeck('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.vic.discardSize(), 1)
        self.assertIsNotNone(self.vic.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
