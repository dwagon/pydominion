#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Stables(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """You may discard a Treasure. If you do, +3 Cards and +1 Action."""
        self.name = 'Stables'
        self.cost = 5

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        tr = player.plrDiscardCards(cardsrc=treasures, prompt="Discard a card and get +3 Cards +1 Action")
        if tr:
            player.addActions(1)
            player.pickupCards(3)


###############################################################################
class Test_Stables(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Stables'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Stables'].remove()

    def test_play(self):
        """ Play duchess - keep on deck """
        self.plr.setHand('Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
