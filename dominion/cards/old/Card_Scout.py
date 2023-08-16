#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Scout(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+1 action, Adjust top 4 cards of deck"
        self.name = "Scout"
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Reveal the top 4 cards of your deck. Put the revealed
        victory cards into your hand. Put the other cards on top
        of your deck in any order"""
        # TODO: Currently you can't order the cards you return
        cards = []
        for _ in range(4):
            c = player.next_card()
            player.reveal_card(c)
            if c.isVictory():
                player.add_card(c, Piles.HAND)
                player.output(f"Adding {c.name} to hand")
            else:
                cards.append(c)
        for c in cards:
            player.output(f"Putting {c.name} back on deck")
            player.add_card(c, "deck")


###############################################################################
class Test_Scout(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Scout"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.scout = self.g["Scout"].remove()

    def test_play(self):
        self.plr.add_card(self.scout, Piles.HAND)
        self.plr.play_card(self.scout)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_victory(self):
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.scout, Piles.HAND)
        self.plr.play_card(self.scout)
        for c in self.plr.piles[Piles.HAND]:
            self.assertTrue(c.isVictory())

    def test_deck(self):
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.scout, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Duchy")
        self.plr.play_card(self.scout)
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Duchy")
        for c in self.plr.piles[Piles.DECK]:
            self.assertEqual(c.name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
