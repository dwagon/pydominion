#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sleigh """

import unittest
import Game
import Card


###############################################################################
class Card_Sleigh(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.MENAGERIE
        self.desc = """Gain 2 Horses. When you gain a card, you may discard this,
            to put that card into your hand or onto your deck."""
        self.name = 'Sleigh'
        self.cost = 2
        self.required_cards = [('Card', 'Horse')]

    def special(self, game, player):
        player.gainCard('Horse')
        player.gainCard('Horse')

    def hook_gain_card(self, game, player, card):
        # Discard self if choice == hand or deck
        choice = player.plrChooseOptions(
            "What to do with {}?".format(card.name),
            ("Discard by default", 'discard'),
            ("Put into hand and discard Sleigh", 'hand'),
            ("Put onto your deck and discard Sleigh", 'deck')
        )
        if choice != 'discard':
            player.discardCard(self)
        return {'destination': choice}


###############################################################################
class Test_Sleigh(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Sleigh'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Sleigh'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a supplies """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.deck[-1].name, 'Horse')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
