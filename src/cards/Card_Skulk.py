#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Skulk(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_DOOM]
        self.base = Game.NOCTURNE
        self.name = 'Skulk'
        self.buys = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            return "+1 Buy; Each other player receives the next Hex; When you gain this, gain a Gold."
        return "+1 Buy; Each other player receives the next Hex."

    def hook_gain_this_card(self, game, player):
        player.gainCard('Gold')

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.output("{}'s Skulk hexed you".format(player.name))
            plr.receive_hex()


###############################################################################
class Test_Skulk(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Skulk'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.Skulk = self.g['Skulk'].remove()
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_card(self):
        """ Play Skulk """
        self.plr.addCard(self.Skulk, 'hand')
        self.plr.playCard(self.Skulk)
        self.assertTrue(self.vic.has_state('Deluded'))

    def test_gain(self):
        self.plr.gainCard('Skulk')
        self.assertIsNotNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
