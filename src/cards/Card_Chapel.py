#!/usr/bin/env python

import unittest
from Card import Card


class Card_Chapel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash up to 4 cards"
        self.name = 'Chapel'
        self.cost = 2

    def special(self, game, player):
        """ Trash up to 4 cards from your hand """
        trash = []
        player.output("Trash up to four cards")
        while(1):
            options = [{'selector': '0', 'print': 'Finish trashing', 'card': None}]
            index = 1
            for c in player.hand:
                sel = "%d" % index
                trashtag = 'Untrash' if c in trash else 'Trash'
                pr = "%s %s" % (trashtag, c.name)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1
            o = player.userInput(options, "Trash which card?")
            if not o['card']:
                break
            if o['card'] in trash:
                trash.remove(o['card'])
            else:
                if len(trash) < 4:
                    trash.append(o['card'])
                else:
                    player.output("Can only trash four cards")

        for t in trash:
            player.output("Trashing %s" % t.name)
            player.trashCard(t)


###############################################################################
class Test_Chapel(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['chapel'])
        self.plr = self.g.players[0]
        self.ccard = self.g['chapel'].remove()
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_trashnone(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.plr.hand), 3)
        self.assertEquals(self.g.trashpile, [])

    def test_trashtwo(self):
        self.plr.test_input = ['1', '2', '0']
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.plr.hand), 1)
        self.assertEquals(len(self.g.trashpile), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
