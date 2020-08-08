#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Messenger(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.ADVENTURE
        self.name = 'Messenger'
        self.buys = 1
        self.coin = 2
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            return """+1 Buy, +2 Coin, You may put your deck into your discard pile;
                When this is your first buy in a turn, gain a card costing up to 4,
                and each other player gains a copy of it."""
        return "+1 Buy, +2 Coin, You may put your deck into your discard pile"

    def special(self, game, player):
        o = player.plrChooseOptions(
            'Put entire deck into discard pile?',
            ('No - keep it as it is', False),
            ('Yes - dump it', True)
            )
        if o:
            for c in player.deck[:]:
                player.addCard(c, 'discard')
                player.deck.remove(c)

    def hook_buy_this_card(self, game, player):
        if len(player.stats['bought']) == 1:
            c = player.plrGainCard(4, prompt="Pick a card for everyone to gain")
            for plr in game.player_list():
                if plr != player:
                    plr.gainCard(newcard=c)
                    plr.output("Gained a %s from %s's Messenger" % (c.name, player.name))


###############################################################################
class Test_Messenger(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Messenger'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g['Messenger'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Messenger - do nothing"""
        self.plr.test_input = ['No']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_discard(self):
        """ Play a messenger and discard the deck """
        decksize = self.plr.deckSize()
        self.plr.test_input = ['Yes']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.discard_size(), decksize)

    def test_buy(self):
        """ Buy a messenger """
        self.plr.test_input = ['get silver']
        self.plr.setCoin(4)
        self.plr.buyCard(self.g['Messenger'])
        for plr in self.g.player_list():
            self.assertIsNotNone(plr.in_discard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
