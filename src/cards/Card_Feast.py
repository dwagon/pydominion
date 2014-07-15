#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Feast(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash this card, Gain a card costing up to 5"
        self.name = 'Feast'
        self.cost = 4

    def special(self, game, player):
        """ Trash this card. Gain a card costing up to 5 """
        if self.trashCard(player):
            self.selectNewCard(game, player)

    def selectNewCard(self, game, player):
        player.output("Gain a card costing up to 5")
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        buyable = player.cardsUnder(5)
        index = 1
        for p in buyable:
            selector = "%d" % index
            toprint = 'Get %s (%d coin)' % (p.name, p.cost)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = player.userInput(options, "What card do you wish?")
        if o['card']:
            player.gainCard(o['card'])
            player.output("Took %s" % o['card'].name)
        return

    def trashCard(self, player):
        ans = player.plrChooseOptions(
            "Trash this card?",
            ("Don't trash this card", False), ("Trash this card", True))
        if ans:
            player.trashCard(self)
            return True
        return False


###############################################################################
class Test_Feast(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['feast'])
        self.plr = list(self.g.players.values())[0]

    def test_dontTrash(self):
        self.plr.setHand('feast')
        self.plr.test_input = ['0']
        self.plr.playCard(self.plr.hand[0])
        self.assertEquals(self.g.trashpile, [])
        self.assertEquals(self.plr.played[0].name, 'Feast')

    def test_trashForNothing(self):
        self.plr.setHand('feast')
        self.plr.test_input = ['1', '0']
        self.plr.playCard(self.plr.hand[0])
        self.assertEquals(self.plr.hand, [])
        self.assertEquals(self.g.trashSize(), 1)
        self.assertEquals(self.g.trashpile[0].name, 'Feast')
        self.assertEquals(self.plr.played, [])

    def test_trashForSomething(self):
        self.plr.setHand('feast')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.plr.hand[0])
        self.assertEquals(self.g.trashSize(), 1)
        self.assertEquals(self.g.trashpile[0].name, 'Feast')
        self.assertEquals(self.plr.played, [])
        self.assertEquals(self.plr.discardSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
