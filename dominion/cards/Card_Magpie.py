#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Magpie(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ADVENTURE
        self.desc = """+1 Card; +1 Action; Reveal the top card of your deck.
            If it's a Treasure, put it into your hand. If it's an Action or
            Victory card, gain a Magpie."""
        self.name = "Magpie"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Reveal the top card of your deck. If it's a treasure, put it into your
        hand. If it's an Action or Victory card, gain a Magpie"""
        c = player.nextCard()
        player.reveal_card(c)
        if c.isTreasure():
            player.output("Putting revealed %s into hand" % c.name)
            player.addCard(c, "hand")
        else:
            player.addCard(c, "deck")
            if c.isAction() or c.isVictory():
                player.output("Revealed %s so gaining magpie" % c.name)
                player.gainCard("Magpie")


###############################################################################
class Test_Magpie(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Magpie"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Magpie"].remove()

    def test_treasure(self):
        """Play a magpie with treasure"""
        self.plr.setDeck("Gold", "Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        # Hand of 5, the card gained and the treasure
        self.assertEqual(self.plr.hand.size(), 5 + 1 + 1)
        self.assertTrue(self.plr.in_hand("Gold"))

    def test_victory(self):
        """Play a magpie with treasure"""
        self.plr.setDeck("Duchy", "Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        # Hand of 5, the card gained
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertFalse(self.plr.in_hand("Duchy"))
        self.assertEqual(self.plr.discardpile[0].name, "Magpie")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
