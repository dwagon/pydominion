#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Torturer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.ATTACK]
        self.base = Game.INTRIGUE
        self.desc = "+3 cards; Other players discard 2 cards or gain a curse"
        self.required_cards = ['Curse']
        self.name = 'Torturer'
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """ Each other player chooses one: he discards 2 cards; or
            he gains a Curse card, putting it in his hand """
        for plr in player.attackVictims():
            plr.output("Choose:")
            self.choiceOfDoom(plr, player)

    def choiceOfDoom(self, victim, player):
        victim.output("Your hand is: %s" % ", ".join([c.name for c in victim.hand]))
        discard = victim.plrChooseOptions(
            "Discard or curse",
            ('Discard 2 cards', True),
            ('Gain a curse card', False))
        if discard:
            player.output("%s discarded" % victim.name)
            victim.plrDiscardCards(2)
        else:
            player.output("%s opted for a curse" % victim.name)
            victim.gainCard('Curse', 'hand')


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if kind == 'cards':
        return player.pick_to_discard(2)
    if kind == 'choices':
        return True     # Discard
    return False


###############################################################################
class Test_Torturer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Torturer', 'Moat'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Torturer'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_opt_curse(self):
        """ Play the torturer - victim opts for a curse"""
        self.victim.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 8)
        self.assertTrue(self.victim.in_hand('Curse'))

    def test_opt_discard(self):
        """ Play the torturer - victim opts for discarding"""
        self.victim.test_input = ['0', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 8)
        self.assertEqual(self.victim.handSize(), 3)
        self.assertFalse(self.victim.in_hand('Curse'))

    def test_defended(self):
        """ Defending against a torturer """
        self.victim.setHand('Moat')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 8)
        self.assertEqual(self.victim.handSize(), 1)
        self.assertFalse(self.victim.in_hand('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
