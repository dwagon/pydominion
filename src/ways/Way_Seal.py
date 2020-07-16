#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Seal(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "+1 Coin; This turn, when you gain a card, you may put it onto your deck."
        self.name = "Seal"

    def special(self, game, player):
        player.addCoin(1)
        player.add_hook('gain_card', self.gain_card)

    def gain_card(self, game, player, card):
        mod = {}
        deck = player.plrChooseOptions(
            "Seal: Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True))
        if deck:
            player.output("Putting %s on deck due to Way of the Seal" % card.name)
            mod['destination'] = 'topdeck'
        return mod


###############################################################################
class Test_Seal(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Seal'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()

    def test_play(self):
        """ Perform a Seal """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Seal', 'top of deck']
        self.plr.playCard(self.card)
        self.plr.gainCard('Gold')
        self.g.print_state()
        self.assertEqual(self.plr.deck[-1].name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
