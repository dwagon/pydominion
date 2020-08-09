#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Falconer """

import unittest
import Game
import Card


###############################################################################
class Card_Falconer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.MENAGERIE
        self.desc = """Gain a card to your hand costing less than this. When any
            player gains a card with 2 or more types (Action, Attack, etc.), you
            may play this from your hand."""
        self.name = 'Falconer'
        self.cost = 5

    def special(self, game, player):
        player.plrGainCard(5)

    def hook_gain_card(self, game, player, card):
        if len(card.get_cardtype_repr().split(',')) >= 2:
            player.output("Falconer lets you gain a card")
            player.plrGainCard(5)


###############################################################################
class Test_Falconer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Falconer', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Falconer'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a card """
        self.plr.test_input = ['Get Silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Silver'))

    def test_gaincard(self):
        """ Gain a card """
        self.plr.test_input = ['Get Silver']
        self.plr.gainCard('Moat')
        self.g.print_state()
        self.assertIsNotNone(self.plr.in_discard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
