#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Inn(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.name = 'Inn'
        self.cards = 2
        self.actions = 2
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return """+2 Cards, +2 Actions, Discard 2 cards.
            When you gain this, look through your discard pile
            (including this), reveal any number of Action cards
            from it, and shuffle them into your deck."""
        else:
            return "+2 Cards, +2 Actions, Discard 2 cards"

    def special(self, game, player):
        player.plrDiscardCards(num=2, force=True)

    def hook_gainThisCard(self, game, player):
        cards = []
        for card in player.discardpile[:]:
            if card.isAction():
                cards.append(card)
        if not cards:
            player.output("No suitable cards in discardpile")
            return {}
        back = player.cardSel(anynum=True, prompt="Select cards to shuffle back into your deck", cardsrc=cards)
        for card in back:
            player.discardpile.remove(card)
            player.addCard(card, 'deck')
            player.deck.shuffle()
        return {}


###############################################################################
class Test_Inn(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Inn', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Inn'].remove()

    def test_play(self):
        """ Play the card """
        self.plr.setHand('Duchy', 'Province', 'Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Duchy', 'Province', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 4 + 2 - 2)
        self.assertEqual(self.plr.getActions(), 2)

    def test_gain(self):
        self.plr.setDiscard('Moat', 'Gold')
        self.plr.test_input = ['Moat', 'finish']
        self.plr.gainCard('Inn')
        self.assertIsNotNone(self.plr.inDeck('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
