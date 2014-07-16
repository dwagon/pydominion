#!/usr/bin/env python

import unittest
from Card import Card


class Card_Lookout(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = "Look at the top 3 cards of your deck. Trash 1, Discard 1, Deck 1"
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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['lookout'])
        self.plr = self.g.playerList(0)
        self.lookout = self.g['lookout'].remove()

    def test_actions(self):
        self.plr.setDeck('copper', 'estate', 'gold', 'province')
        self.plr.addCard(self.lookout, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.lookout)
        self.assertEqual(self.g.trashpile[0].name, 'Province')
        self.assertEqual(self.plr.discardpile[0].name, 'Gold')
        self.assertEqual(self.plr.deck[0].name, 'Copper')
        self.assertEqual(self.plr.deck[1].name, 'Estate')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
