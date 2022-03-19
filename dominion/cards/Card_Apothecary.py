#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Apothecary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALCHEMY
        self.desc = "+1 card, +1 action, Take coppers and potions out of top 4 of deck"
        self.name = "Apothecary"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.potcost = True
        self.required_cards = ["Potion"]

    def special(self, game, player):
        """Reveal the top 4 cards of your deck. Put the revealed
        Coppers and Potions into your hand. Put the other cards
        back on top of your deck in any order"""
        unput = []
        for _ in range(4):
            c = player.next_card()
            player.reveal_card(c)
            if c.name in ("Copper", "Potion"):
                player.output(f"Putting {c.name} in hand")
                player.add_card(c, "hand")
            else:
                unput.append(c)
        for c in unput:
            player.output(f"Putting {c.name} back in deck")
            player.add_card(c, "deck")


###############################################################################
class Test_Apothecary(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Apothecary"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_none(self):
        self.plr.set_hand("Apothecary")
        apoth = self.plr.hand[0]
        self.plr.set_deck("Duchy", "Estate", "Estate", "Estate", "Province")
        self.plr.play_card(apoth)
        self.assertEqual(self.plr.hand.size(), 1)  # P
        self.assertEqual(self.plr.deck.size(), 4)  # D + E + E + E

    def test_some(self):
        self.plr.set_hand("Apothecary")
        apoth = self.plr.hand[0]
        self.plr.set_deck("Duchy", "Potion", "Copper", "Estate", "Province")
        self.plr.play_card(apoth)
        self.assertEqual(self.plr.hand.size(), 3)  # P + C + Pot
        self.assertEqual(self.plr.deck.size(), 2)  # E + D


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
