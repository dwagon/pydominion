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

        card = player.plrGainCard(len(cards), prompt="Gain a card costing up to %d. If it is a victory then this card will be trashed" % len(cards))
        if card and card.isVictory():
            player.trashCard(self)


###############################################################################
class Test_Hornofplenty(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Horn of Plenty', 'Moat'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Horn of Plenty'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Horn of Plenty """
        self.plr.setPlayed('Copper', 'Silver', 'Silver')
        self.plr.test_input = ['Get Silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inPlayed('Horn of Plenty'))

    def test_play_victory(self):
        """ Horn of Plenty - gaining a victory card """
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Moat')
        self.plr.test_input = ['Get Duchy']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertIsNone(self.plr.inPlayed('Horn of Plenty'))
        self.assertIsNotNone(self.g.in_trash('Horn of Plenty'))

    def test_play_nothing(self):
        """ Horn of Plenty - gaining nothing """
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Moat')
        self.plr.test_input = ['finish selecting']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.inDiscard('Duchy'))
        self.assertIsNotNone(self.plr.inPlayed('Horn of Plenty'))
        self.assertIsNone(self.g.in_trash('Horn of Plenty'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
