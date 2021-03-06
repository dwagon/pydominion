#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Farmingvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.CORNUCOPIA
        self.desc = """+2 actions. Reveal cards from the top of your deck until
            you reveal an Action or Treasure card. Put that card into your hand
            and discard the other cards."""
        self.name = 'Farming Village'
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        """ Reveal cards from the top of your deck until you revel
            an Action or Treasure card. Put that card into your hand
            and discard the other cards. """
        while True:
            c = player.nextCard()
            player.revealCard(c)
            if c.isTreasure() or c.isAction():
                player.output("Added %s to hand" % c.name)
                player.addCard(c, 'hand')
                break
            player.output("Picked up and discarded %s" % c.name)
            player.discardCard(c)


###############################################################################
class Test_Farmingvillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Farming Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Farming Village'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_treasure(self):
        """ Play farming village with a treasure in deck """
        self.plr.setDeck('Estate', 'Estate', 'Silver', 'Estate', 'Estate')
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.in_hand('Silver'))
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Estate')

    def test_play_action(self):
        """ Play farming village with an action in deck"""
        self.plr.setDeck('Estate', 'Estate', 'Farming Village', 'Estate', 'Estate')
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.in_hand('Farming Village'))
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Estate')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
