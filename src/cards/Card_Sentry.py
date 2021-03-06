#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sentry """

import unittest
import Game
import Card


###############################################################################
class Card_Sentry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = """+1 Card; +1 Action; Look at the top 2 cards of your deck.
            Trash and/or discard any number of them. Put the rest back on top
            in any order."""
        self.name = 'Sentry'
        self.cost = 5
        self.cards = 1
        self.actions = 1

    def special(self, game, player):
        cards = [player.nextCard() for _ in range(2)]
        player.output("Look at the top two cards of your deck. Trash, discard or move to deck")
        player.output("Trash any/all of {}".format(self.names(cards)))
        to_trash = player.plrTrashCard(cardsrc=cards, num=2)
        cards = [_ for _ in cards if _ not in to_trash]
        if not cards:
            return
        player.output("Discard any/all of {}".format(self.names(cards)))
        to_discard = player.plrDiscardCards(cardsrc=cards, num=2)
        to_deck = [player.addCard(_, 'topdeck') for _ in cards if _ not in to_discard]
        if to_deck:
            player.output("Moving {} to the deck".format(self.names(to_deck)))

    def names(self, cards):
        return ", ".join([_.name for _ in cards])


###############################################################################
class Test_Sentry(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Sentry'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Sentry'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_trash_discard(self):
        self.plr.setDeck('Copper', 'Province', 'Duchy')
        self.plr.test_input = ["Trash Copper", "Finish", "Discard Province", "Finish"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Copper'))
        self.assertIsNotNone(self.plr.in_discard('Province'))

    def test_discard_keep(self):
        self.plr.setDeck('Gold', 'Province', 'Duchy')
        self.plr.test_input = ["Finish", "Discard Province", "Finish"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Province'))
        self.assertIsNotNone(self.plr.in_deck('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
