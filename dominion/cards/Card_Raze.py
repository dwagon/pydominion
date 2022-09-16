#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Raze(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action; Trash this or a card from your hand. Look at a number
            of cards from the top of your deck equal to the cost in Coin of the
            trashed card. Put one into your hand and discard the rest """
        self.name = "Raze"
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """Trash this or a card from your hand. Look at a number of cards
        from the top of your deck equal to the cost in Coin of the trashed
        card. Put one into your hand and discard the rest"""
        cards_to_trash = [self]
        for c in player.hand:
            cards_to_trash.append(c)
        trash = player.plr_trash_card(cardsrc=cards_to_trash, force=True)
        cost = trash[0].cost
        if cost:
            cards = []
            for c in range(cost):
                cards.append(player.next_card())
            ans = player.card_sel(
                force=True, prompt="Pick a card to put into your hand", cardsrc=cards
            )
            for c in cards:
                if c == ans[0]:
                    player.add_card(c, "hand")
                else:
                    player.add_card(c, "discard")


###############################################################################
class Test_Raze(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Raze"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Raze"].remove()

    def test_play(self):
        """Play a raze - trashing itself"""
        self.plr.add_card(self.card, "hand")
        self.plr.deck.set("Silver", "Gold", "Province")
        self.plr.test_input = ["Raze", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIn("Province", self.plr.discardpile)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Silver", self.plr.deck)
        self.assertIn("Raze", self.g.trashpile)

    def test_copper(self):
        """Play a raze - trashing copper - a zero value card"""
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.deck.set("Silver", "Gold", "Province")
        self.plr.test_input = ["Copper", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
