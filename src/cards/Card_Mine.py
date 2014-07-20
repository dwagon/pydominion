#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Mine(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash a treasure, gain a better treasure"
        self.name = 'Mine'
        self.cost = 5

    def special(self, game, player):
        """ Trash a treasure card from your hand. Gain a treasure card
            costing up to 3 more, put it in your hand """
        options = [{'selector': '0', 'print': "Don't trash a card", 'card': None}]
        index = 1
        for c in player.hand:
            if c.isTreasure():
                sel = "%s" % index
                options.append({'selector': sel, 'print': "Trash %s" % c.name, 'card': c})
                index += 1
        player.output("Trash a treasure to gain a better one")
        o = player.userInput(options, "Trash which treasure?")
        if o['card']:
            val = o['card'].cost
            # Make an assumption and pick the best treasure card
            # TODO - let user pick
            for tc in game.baseCards:
                if game[tc].cost == val + 3:
                    c = player.gainCard(tc, 'hand')
                    player.output("Converted to %s" % c.name)
                    player.trashCard(o['card'])
                    break
            else:   # pragma: no cover
                player.output("No appropriate treasure card exists")


###############################################################################
class Test_Mine(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['mine'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['mine'].remove()

    def test_convcopper(self):
        self.plr.setHand('copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.hand[0].name, 'Silver')
        self.assertTrue(self.plr.discardpile.isEmpty())
        self.assertEquals(self.plr.handSize(), 1)
        self.assertEquals(self.plr.getCoin(), 0)
        self.assertEquals(self.plr.getBuys(), 1)
        self.assertEquals(self.plr.getActions(), 0)

    def test_convnothing(self):
        self.plr.setHand('copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.hand[0].name, 'Copper')
        self.assertTrue(self.plr.discardpile.isEmpty())
        self.assertEquals(self.plr.handSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
