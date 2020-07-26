#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Herald(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'guilds'
        self.name = 'Herald'
        self.overpay = True
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            return """+1 Card +1 Action. Reveal the top card of your deck.
                If it is an Action, play it.  When you buy this, you may overpay
                for it. For each Coin you overpaid, look through your discard pile
                and put a card from it on top of your deck."""
        return "+1 Card +1 Action. Reveal the top card of your deck. If it is an Action, play it."

    def special(self, game, player):
        card = player.nextCard()
        player.revealCard(card)
        if card.isAction():
            player.addCard(card, 'hand')
            player.playCard(card, costAction=False)

    def hook_overpay(self, game, player, amount):
        for _ in range(amount):
            card = player.cardSel(
                num=1, force=True, cardsrc='discard',
                prompt="Look through your discard pile and put a card from it on top of your deck"
            )
            player.addCard(card[0], 'topdeck')
            player.discardpile.remove(card[0])


###############################################################################
class Test_Herald(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Herald', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Herald'].remove()

    def test_play(self):
        """ Play a Herald """
        self.plr.setDeck('Moat', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1 + 1)
        self.assertIsNotNone(self.plr.inPlayed('Moat'))

    def test_buy(self):
        """ Buy a Herald """
        self.plr.coin = 5
        self.plr.test_input = ['1', 'moat']
        self.plr.setDiscard('Estate', 'Moat', 'Copper')
        self.plr.buyCard(self.g['Herald'])
        self.assertEqual(self.plr.deck[-1].name, 'Moat')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
