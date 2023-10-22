#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


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
        for c in player.piles[Piles.HAND]:
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
                    player.add_card(c, Piles.HAND)
                else:
                    player.add_card(c, "discard")


###############################################################################
class Test_Raze(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Raze"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Raze")

    def test_play(self):
        """Play a raze - trashing itself"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province")
        self.plr.test_input = ["Raze", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Raze", self.g.trash_pile)

    def test_copper(self):
        """Play a raze - trashing copper - a zero value card"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province")
        self.plr.test_input = ["Copper", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
