#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Miller(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TOWNSFOLK]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.actions = 1
        self.name = "Miller"
        self.desc = """+1 Action; Look at the top 4 cards of your deck. Put one into your hand and discard the rest."""

    def special(self, game, player):
        cards = []
        for _ in range(4):
            card = player.next_card()
            cards.append(card)
        ch = player.card_sel(prompt="Pick a card to put into your hand", cardsrc=cards)
        player.add_card(ch[0], "hand")
        cards.remove(ch[0])
        for card in cards:
            player.add_card(card, "discard")


###############################################################################
class Test_Miller(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g["Townsfolk"].remove()
            if self.card.name == "Miller":
                break
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a miller"""
        self.plr.deck.set("Silver", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertNotIn("Silver", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
