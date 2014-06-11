#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Secretchamber(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'intrigue'
        self.desc = "Discard any number of cards; +1 gold per card discarded"
        self.name = 'Secret Chamber'
        self.cost = 2

    def special(self, player, game):
        """ Discard any number of cards, +1 gold per card discarded"""
        player.output("Select which card(s) to discard (+1 gold per discard)?")
        todiscard = player.plrDiscardCards(anynum=True)
        player.t['gold'] += len(todiscard)

    def hook_underAttack(self, player, game):
        """ When another player plans an Attack card, you may reveal
            this from you hand. If you do +2 cards, then put 2 cards
            from your hand on top of your deck """
        if not self.revealCard(player):
            return
        player.pickupCards(2)
        player.output("Put two cards onto deck")
        for i in range(2):
            self.deckCard(player)

    def deckCard(self, player):
        options = []
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Put %s to top of deck" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Deck which card?")
        player.addCard(o['card'], 'deck')
        player.hand.remove(o['card'])

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['secretchamber'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['secretchamber'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_none(self):
        """ Play the Secret Chamber - discard none"""
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.t['gold'], 0)

    def test_play_three(self):
        """ Play the Secret Chamber - discard three"""
        self.plr.test_input = ['1', '2', '3', '0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 2)
        self.assertEqual(self.plr.t['gold'], 3)

    def test_underattack(self):
        """ Secret chamber is under attack """
        # TODO
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
