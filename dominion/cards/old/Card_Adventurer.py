#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Adventurer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Dig through deck for two treasures"
        self.name = "Adventurer"
        self.cost = 6

    def special(self, game, player):
        """Reveal cards from your deck until you reveal two treasure cards
        Add those to your hand and discard the other revealed cards"""
        treasures = []
        while len(treasures) < 2:
            c = player.pickup_card(verbose=False)
            player.reveal_card(c)
            if c.isTreasure():
                treasures.append(c)
                player.output("Adding %s" % c.name)
            else:
                player.discard_card(c)
                player.output("Discarding %s as not treasure" % c.name)


###############################################################################
class Test_Adventurer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Adventurer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_treasures(self):
        self.plr.deck.set("Copper", "Silver", "Gold", "Estate")
        self.plr.hand.set("Adventurer")
        self.plr.play_card(self.plr.hand[0])
        self.assertEqual(sorted(["Silver", "Gold"]), sorted([c.name for c in self.plr.hand]))
        self.assertIsNotNone(self.plr.discardpile["Estate"])
        self.assertEqual(self.plr.deck[0].name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
