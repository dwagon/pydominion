#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pixie(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.base = 'nocturne'
        self.desc = "+1 Card; +1 Action; Discard the top Boon. You may trash this to receive that Boon twice."
        self.name = 'Pixie'
        self.cost = 2
        self.actions = 1
        self.cards = 1
        self.heirloom = 'Goat'

    def special(self, game, player):
        topboon = game.receive_boon()
        opt = player.plrChooseOptions(
                "Either:",
                ("Discard {}".format(topboon.name), False),
                ("Trash Pixie to get {} twice ({})".format(topboon.name, topboon.description(player)), True)
                )
        if opt:
            player.trashCard(self)
            player.receive_boon(boon=topboon, discard=False)
            player.receive_boon(boon=topboon)


###############################################################################
class Test_Pixie(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Pixie'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Pixie'].remove()

    def test_play_keep(self):
        """ Play a Pixie """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Discard The']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)

    def test_trash(self):
        """ Play a Pixie and trash it"""
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.discardSize(), 2)
            for c in self.plr.discardpile:
                self.assertEqual(c.name, 'Silver')
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
