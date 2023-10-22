#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Harbinger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1 Card; +1 Action; Look through your discard pile. You may put a card from it onto your deck."
        self.name = "Harbinger"
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game, player):
        index = 1
        options = [{"selector": "0", "print": "Don't look through discard pile", "card": None}]
        already = []
        for c in player.piles[Piles.DISCARD]:
            sel = f"{index}"
            pr = f"Put {c.name} back in your deck"
            if c.name in already:
                continue
            options.append({"selector": sel, "print": pr, "card": c})
            already.append(c.name)
            index += 1
        if not already:
            player.output("No suitable cards")
            return
        player.output("Look through your discard pile. You may put a card from it onto your deck.")
        o = player.user_input(options, "Which Card? ")
        if not o["card"]:
            return
        player.add_card(o["card"], "topdeck")
        player.piles[Piles.DISCARD].remove(o["card"])


###############################################################################
class Test_Harbinger(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Harbinger"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Harbinger")

    def test_play(self):
        """Play a harbinger"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Province")
        self.plr.test_input = ["Put Gold"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
