#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Animal_Fair """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Animal_Fair(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'menagerie'
        self.desc = """+4 Coin; +1 Buy per empty supply pile.
            Instead of paying this card's cost, you may trash an Action card
            from your hand."""
        self.name = 'Animal Fair'
        self.coin = 4
        self.always_buyable = True
        self.cost = 7

    def special(self, game, player):
        empties = sum([1 for st in game.cardpiles if game[st].isEmpty()])
        player.addBuys(empties)

    def hook_buy_this_card(self, game, player):
        actions = [_ for _ in player.hand if _.isAction()]
        if not actions:
            return 0
        tc = player.plrTrashCard(prompt="Trash card to get Animal Fair for free", cardsrc=actions)
        if tc:
            return -7
        return 0


###############################################################################
class Test_Animal_Fair(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Animal Fair'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Animal Fair'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a supplies """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.deck[-1].name, 'Horse')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
