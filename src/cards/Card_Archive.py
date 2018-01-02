#!/usr/bin/env python

from Card import Card
from PlayArea import PlayArea
import unittest


###############################################################################
class Card_Archive(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'empires'
        self.desc = "+1 Action; Set aside the top 3 cards of your deck face down (you may look at them). Now and at the start of your next two turns, put one into your hand."
        self.name = 'Archive'
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        if not hasattr(player, '_archive_reserve'):
            player._archive_reserve = PlayArea([])
        for i in range(3):
            card = player.nextCard()
            player.output("Putting {} in the archive".format(card.name))
            player._archive_reserve.add(card)
            player.secret_count += 1
        self.permanent = True

    def duration(self, game, player):
        options = []
        index = 0
        for card in player._archive_reserve:
            sel = "{}".format(index)
            toprint = "Bring back {}".format(card.name)
            options.append({'selector': sel, 'print': toprint, 'card': card})
            index += 1
        o = player.userInput(options, "What card to bring back from the Archive?")
        player.addCard(o['card'], 'hand')
        player._archive_reserve.remove(o['card'])
        player.secret_count -= 1
        if player._archive_reserve.isEmpty():
            self.permanent = False


###############################################################################
class Test_Archive(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Archive'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Archive'].remove()

    def test_play(self):
        """ Play a Archive """
        self.plr.setDeck('Gold', 'Silver', 'Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.plr.endTurn()
        self.plr.test_input = ['Bring back Gold']
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertEqual(len(self.plr._archive_reserve), 2)
        self.plr.endTurn()
        self.plr.test_input = ['Bring back Silver']
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inHand('Silver'))
        self.plr.endTurn()
        self.plr.test_input = ['Bring back Province']
        self.plr.startTurn()
        self.assertFalse(self.card.permanent)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF