#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Secretchamber(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'intrigue'
        self.desc = "Discard any number of cards; +1 coin per card discarded"
        self.name = 'Secret Chamber'
        self.cost = 2

    def special(self, player, game):
        """ Discard any number of cards, +1 coin per card discarded"""
        todiscard = player.plrDiscardCards(anynum=True, prompt="Select which card(s) to discard (+1 coin per discard)?")
        player.addCoin(len(todiscard))

    def hook_underAttack(self, player, game):
        """ When another player plays an Attack card, you may reveal
            this from you hand. If you do +2 cards, then put 2 cards
            from your hand on top of your deck """
        if not self.revealCard(player):
            return
        player.pickupCards(2)
        player.output("Put two cards onto deck")
        cards = player.cardSel(
            prompt='Put which two cards on top of deck?',
            force=True, num=2, verbs=('Put', 'Unput'))
        for card in cards:
            player.addCard(card, 'topdeck')
            player.hand.remove(card)

    def revealCard(self, player):
        options = [
            {'selector': '0', 'print': "Don't reveal", 'reveal': False},
            {'selector': '1', 'print': 'Reveal', 'reveal': True}
        ]
        o = player.userInput(options, "Reveal Secret Chamber?")
        return o['reveal']


###############################################################################
class Test_Secretchamber(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Secret Chamber'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Secret Chamber'].remove()

    def test_play_none(self):
        """ Play the Secret Chamber - discard none"""
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_play_three(self):
        """ Play the Secret Chamber - discard three"""
        self.plr.setHand('Copper', 'Silver', 'Gold', 'Province', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['discard copper', 'discard silver', 'discard gold', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getCoin(), 3)

    def test_underattack(self):
        """ Secret chamber is under attack """
        # TODO
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
