#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_SecretPassage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = """+2 Cards; +1 Action; Take a card from your hand and put it anywhere in your deck."""
        self.name = 'Secret Passage'
        self.cost = 4
        self.actions = 1
        self.cards = 2

    def special(self, game, player):
        card = player.cardSel(
            prompt="Take a card from your hand and put into your deck",
            cardsrc='hand'
        )
        if card:
            dest = player.plrChooseOptions(
                "Put {} into top or bottom of deck".format(card[0].name),
                ("Top of deck", "topdeck"),
                ("Bottom of deck", "deck")
            )
            player.addCard(card[0], dest)
            player.hand.remove(card[0])


###############################################################################
class Test_SecretPassage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Secret Passage', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Secret Passage'].remove()

    def test_play(self):
        """ Play an Secret Passage """
        self.plr.setHand('Gold', 'Province', 'Duchy', 'Copper', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Select Province', 'Bottom']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.get_actions(), 1)
            self.assertEqual(self.plr.hand.size(), 5 + 2 - 1)    # Hand + SP - back on deck
            self.assertEqual(self.plr.deck[0].name, 'Province')
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
