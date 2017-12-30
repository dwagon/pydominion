#!/usr/bin/env python

import unittest
from Card import Card


class Card_Lookout(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = "+1 Action; Look at the top 3 cards of your deck. Trash one of them. Discard one of them. Put the other one on top of your deck"
        self.name = 'Lookout'
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """ Look at the top 3 cards of your deck. Trash one of them.
            Discard one of them. Put the other one on top of your deck
            """
        cards = []
        for i in range(3):
            cards.append(player.nextCard())
        cards = [c for c in cards if c]
        if not cards:
            player.output("No cards available")
            return
        player.output("Pulled %s from deck" % ", ".join([c.name for c in cards]))
        player.output("Trash a card, Discard a card, put a card on your deck")
        tc = self.trash(player, cards)
        cards.remove(tc)
        cd = self.discard(player, cards)
        cards.remove(cd)
        player.output("Putting %s on top of deck" % cards[0].name)
        player.addCard(cards[0], 'topdeck')

    def trash(self, player, cards):
        index = 1
        options = []
        for c in cards:
            sel = "%d" % index
            index += 1
            options.append({'selector': sel, 'print': "Trash %s" % c.name, 'card': c})
        o = player.userInput(options, "Select a card to trash")
        player.trashCard(o['card'])
        return o['card']

    def discard(self, player, cards):
        index = 1
        options = []
        for c in cards:
            sel = "%d" % index
            index += 1
            options.append({'selector': sel, 'print': "Discard %s" % c.name, 'card': c})
        o = player.userInput(options, "Select a card to discard")
        player.discardCard(o['card'])
        return o['card']


###############################################################################
class Test_Lookout(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Lookout'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.lookout = self.g['Lookout'].remove()

    def test_actions(self):
        self.plr.setDeck('Copper', 'Estate', 'Gold', 'Province')
        self.plr.addCard(self.lookout, 'hand')
        self.plr.test_input = ['Province', 'Gold']
        self.plr.playCard(self.lookout)
        self.assertIsNotNone(self.g.inTrash('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertEqual(self.plr.deck[0].name, 'Copper')
        self.assertEqual(self.plr.deck[1].name, 'Estate')

    def test_nocards(self):
        """ Play a lookout when there are no cards available """
        tsize = self.g.trashSize()
        self.plr.setDeck()
        self.plr.addCard(self.lookout, 'hand')
        self.plr.playCard(self.lookout)
        self.assertEqual(self.g.trashSize(), tsize)
        self.assertEqual(self.plr.discardSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
