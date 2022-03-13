#!/usr/bin/env python

import unittest
import Game
import Card


class Card_Scout(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
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
                player.addCard(c, "hand")
                player.output("Adding %s to hand" % c.name)
            else:
                cards.append(c)
        for c in cards:
            player.output("Putting %s back on deck" % c.name)
            player.addCard(c, "deck")


###############################################################################
class Test_Scout(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Scout"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.scout = self.g["Scout"].remove()

    def test_play(self):
        self.plr.addCard(self.scout, "hand")
        self.plr.playCard(self.scout)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_victory(self):
        self.plr.set_hand()
        self.plr.addCard(self.scout, "hand")
        self.plr.playCard(self.scout)
        for c in self.plr.hand:
            self.assertTrue(c.isVictory())

    def test_deck(self):
        self.plr.set_hand()
        self.plr.addCard(self.scout, "hand")
        self.plr.set_deck("Copper", "Copper", "Copper", "Duchy")
        self.plr.playCard(self.scout)
        self.assertEqual(self.plr.hand[0].name, "Duchy")
        for c in self.plr.deck:
            self.assertEqual(c.name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
