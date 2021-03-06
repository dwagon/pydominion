#!/usr/bin/env python
# pylint: disable=protected-access

import unittest
import Game
import Card
from PlayArea import PlayArea


###############################################################################
class Card_NativeVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.desc = """+2 Actions
        Choose one: Set aside the top card of your deck face down on your
        Native Village mat; or put all the cards from your mat into your hand."""
        self.name = 'Native Village'
        self.base = Game.SEASIDE
        self.actions = 2
        self.cost = 2

    def special(self, game, player):
        if not hasattr(player, '_native_map'):
            player._native_map = PlayArea([])
        player.output("Native Village contains: %s" % ", ".join(c.name for c in player._native_map))
        choice = player.plrChooseOptions(
            "Choose One",
            ("Set aside the top card of your deck face down on your Native Village mat", 'push'),
            ("Put all the cards from your mat into your hand.", 'pull')
            )
        if choice == 'push':
            card = player.nextCard()
            player._native_map.add(card)
            player.output("Adding %s to the Native Village" % card.name)
            player.secret_count += 1
        else:
            self.pull_back(player)

    def hook_end_of_game(self, game, player):
        self.pull_back(player)

    def pull_back(self, player):
        for card in player._native_map[:]:
            player.output("Returning %s from Native Map" % card.name)
            player.addCard(card, 'hand')
            player._native_map.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_NativeVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Native Village'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Native Village'].remove()

    def test_play(self):
        self.plr.setDeck('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Set aside']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr._native_map[0].name, 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Put all']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.secret_count, 0)
        self.assertIsNotNone(self.plr.in_hand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
