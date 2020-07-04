#!/usr/bin/env python

import unittest
from Card import Card
from PlayArea import PlayArea


###############################################################################
class Card_CargoShip(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'renaissance'
        self.name = 'Cargo Ship'
        self.desc = "+2 Coin; Once this turn, when you gain a card, you may set it aside face up (on this). At the start of your next turn, put it into your hand."
        self.cost = 3
        self.coin = 2

    ###########################################################################
    def hook_gainCard(self, game, player, card):
        if not player.inDuration('Cargo Ship'):
            return
        if not player._cargo_ship:
            choice = player.plrChooseOptions(
                "Do you want to set {} aside to play next turn?".format(card.name),
                ("Yes", True),
                ("No", False)
            )
            if choice:
                player._cargo_ship.add(card)
                player.secret_count += 1
                return {'dontadd': True}

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        if not hasattr(player, '_cargo_ship'):
            player._cargo_ship = PlayArea([])

    ###########################################################################
    def duration(self, game, player):
        for card in player._cargo_ship:
            player.addCard(card, 'hand')
            player._cargo_ship.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_CargoShip(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cargo Ship', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_playCard_yes(self):
        self.card = self.g['Cargo Ship'].remove()
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.plr.test_input = ['Yes']
        self.plr.buyCard(self.g['Moat'])
        self.assertEqual(self.plr._cargo_ship[0].name, 'Moat')
        self.plr.end_turn()
        self.plr.startTurn()
        self.assertTrue(self.plr.inHand('Moat'))

    def test_playCard_no(self):
        self.card = self.g['Cargo Ship'].remove()
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.plr.test_input = ['No']
        self.plr.buyCard(self.g['Moat'])
        self.assertEqual(len(self.plr._cargo_ship), 0)
        self.plr.end_turn()
        self.plr.startTurn()
        self.assertIsNone(self.plr.inHand('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
