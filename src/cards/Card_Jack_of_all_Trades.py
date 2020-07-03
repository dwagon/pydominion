#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Jack_of_all_Trades(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = """Gain a Silver.
        Look at the top card of your deck; discard it or put it back.
        Draw until you have 5 cards in your hand.
        You may trash a card from your hand that is not a Treasure."""
        self.name = 'Jack of all Trades'
        self.cost = 4

    def special(self, game, player):
        player.gainCard('Silver')

        card = player.nextCard()
        topdeck = player.plrChooseOptions(
            "Put %s back on top of your deck?" % card.name,
            ("Discard %s" % card.name, False),
            ("Keep %s on top of your deck" % card.name, True))
        if topdeck:
            player.addCard(card, 'topdeck')
        else:
            player.discardCard(card)

        while (player.handSize() < 5):
            player.pickupCard()

        cards = [c for c in player.hand if not c.isTreasure()]
        if cards:
            player.plrTrashCard(cardsrc=cards, prompt="Trash a non-Treasure")


###############################################################################
class Test_Jack_of_all_Trades(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Jack of all Trades'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Jack of all Trades'].remove()

    def test_play(self):
        """ Play a Jack of all Trades"""
        tsize = self.g.trashSize()
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Gold')
        self.plr.setHand('Duchy')
        self.plr.test_input = ['keep', 'duchy']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)

        self.assertIsNotNone(self.plr.inDiscard('Silver'))  # Gain a Silver

        self.assertIsNotNone(self.plr.inHand('Gold'))  # Keep on deck, then picked up

        self.assertEqual(self.plr.handSize(), 5 - 1)    # One trashed
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
