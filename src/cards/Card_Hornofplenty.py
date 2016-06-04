#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Hornofplenty(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'cornucopia'
        self.desc = """When you play this, gain a card costing up to 1 per differently named card you have in play, counting this.
        If it's a Victory card, trash this."""
        self.name = 'Horn of Plenty'
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for c in player.played:
            cards.add(c.name)

        player.output("Gain a card costing up to %d. If it is a victory then this card will be trashed" % len(cards))
        card = player.plrGainCard(len(cards))
        if card.isVictory():
            player.trashCard(self)


###############################################################################
class Test_Hornofplenty(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Horn of Plenty', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Horn of Plenty'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Horn of Plenty """
        self.plr.setPlayed('Copper', 'Silver', 'Silver')
        self.plr.test_input = ['Silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inPlayed('Horn of Plenty'))

    def test_play_victory(self):
        """ Horn of Plenty - gaining a victory card """
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Moat')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertIsNone(self.plr.inPlayed('Horn of Plenty'))
        self.assertIsNotNone(self.g.inTrash('Horn of Plenty'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
