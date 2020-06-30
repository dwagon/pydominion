#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Treasuremap(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = """Trash this and another copy of Treasure Map from your hand.
        If you do trash two Treasure Maps, gain 4 Gold cards, putting them on top of your deck."""
        self.name = 'Treasure Map'
        self.cost = 4

    def special(self, game, player):
        player.trashCard(self)
        tmaps = [c for c in player.hand if c.name == 'Treasure Map'][:1]
        if not tmaps:
            return
        t = player.plrTrashCard(
            prompt="If you trash another treasure map you can get 4 golds",
            cardsrc=tmaps)
        if t:
            player.output("Gaining 4 Gold")
            for i in range(4):
                player.gainCard('Gold', destination='topdeck')
        else:
            player.output("Didn't trash two so no Gold")


###############################################################################
class Test_Treasuremap(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Treasure Map'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Treasure Map'].remove()

    def test_trash(self):
        """ Trash a TM """
        tsize = self.g.trashSize()
        self.plr.setDeck()
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0', '1', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Treasure Map'))
        self.assertEqual(self.plr.deckSize(), 0)

    def test_trash_two(self):
        """ Trash 2 TM """
        tsize = self.g.trashSize()
        self.plr.setDeck()
        self.plr.setHand('Treasure Map')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertIsNotNone(self.g.in_trash('Treasure Map'))
        self.assertEqual(self.plr.deckSize(), 4)
        self.assertIsNotNone(self.plr.inDeck('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
