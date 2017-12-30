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
            ("Keep this card", False), ("Trash this card", True))
        if ans:
            player.trashCard(self)
            return True
        return False


###############################################################################
class Test_Feast(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Feast'], badcards=['Den of Sin', 'Ghost Town', 'Duchess'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Feast'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_dontTrash(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['keep this']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)
        try:
            self.assertEqual(self.plr.played[0].name, 'Feast')
        except AssertionError:
            self.g.print_state()
            raise

    def test_trashForNothing(self):
        tsize = self.g.trashSize()
        try:
            self.plr.test_input = ['trash', 'nothing']
            self.plr.playCard(self.card)
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertIsNotNone(self.g.inTrash('Feast'))
            self.assertTrue(self.plr.played.isEmpty())
        except AssertionError:
            self.g.print_state()
            raise

    def test_trashForSomething(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['trash', 'Get Duchy']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertIsNotNone(self.g.inTrash('Feast'))
            self.assertTrue(self.plr.played.isEmpty())
            self.assertEqual(self.plr.discardSize(), 1)
            self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        except AssertionError:
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
