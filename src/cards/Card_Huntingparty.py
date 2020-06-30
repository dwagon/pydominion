#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Huntingparty(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = """+1 Card +1 Action. Reveal your hand.
        Reveal cards from your deck until you reveal a card that isn't a duplicate of one in your hand.
        Put it into your hand and discard the rest."""
        self.name = 'Hunting Party'
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        discards = []
        for card in player.hand:
            player.revealCard(card)
        while True:
            card = player.nextCard()
            player.revealCard(card)
            if not card:
                player.output("No more cards")
                break
            if player.inHand(card.name):
                player.output("Discarding %s" % card.name)
                discards.append(card)
                continue
            else:
                player.output("Picked up a %s" % card.name)
                player.addCard(card, 'hand')
                break
        for card in discards:
            player.discardCard(card)


###############################################################################
class Test_Huntingparty(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hunting Party'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Hunting Party'].remove()
        self.plr.setHand('Silver', 'Gold')

    def test_playcard(self):
        """ Play a hunting party """
        self.plr.setDeck('Copper', 'Province', 'Silver', 'Gold', 'Duchy')
        self.plr.setHand('Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Duchy'))
        self.assertIsNotNone(self.plr.inHand('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        # Original Hand of 2 + 1 card and 1 non-dupl picked up
        self.assertEqual(self.plr.handSize(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
