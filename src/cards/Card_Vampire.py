#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Vampire(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'attack', 'doom']
        self.base = 'nocturne'
        self.desc = "Each other player receives the next Hex.  Gain a card costing up to 5 other than a Vampire.  Exchange this for a Bat."
        self.name = 'Vampire'
        self.cost = 5
        self.required_cards = [('Card', 'Bat')]

    def night(self, game, player):
        for pl in player.attackVictims():
            pl.output("{}'s Vampire hexed you".format(player.name))
            pl.receive_hex()
        player.plrGainCard(5, exclude=['Vampire'])
        player.replace_card(self, 'Bat')


###############################################################################
class Test_Vampire(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Vampire'], badcards=['Duchess'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Vampire'].remove()
        self.plr.addCard(self.card, 'hand')
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        self.plr.test_input = ['Get Duchy']
        self.plr.phase = 'night'
        self.plr.playCard(self.card)
        self.assertTrue(self.vic.has_state('Deluded'))
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertIsNone(self.plr.inDiscard('Vampire'))
        self.assertIsNotNone(self.plr.inDiscard('Bat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
