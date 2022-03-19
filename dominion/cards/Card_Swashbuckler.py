#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Swashbuckler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """+3 Cards. If your discard pile has any cards in it:
            +1 Coffers, then if you have at least 4 Coffers tokens, take the
            Treasure Chest."""
        self.name = "Swashbuckler"
        self.needsartifacts = True
        self.cards = 3
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        if player.discardpile.size() >= 1:
            player.output("Gained a coffer")
            player.add_coffer(1)
            if player.get_coffers() >= 4:
                if not player.has_artifact("Treasure Chest"):
                    player.output("Gained the Treasure Chest")
                    player.assign_artifact("Treasure Chest")


###############################################################################
class Test_Swashbuckler(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Swashbuckler"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Swashbuckler"].remove()

    def test_play_no_discard(self):
        self.plr.set_coffers(0)
        self.plr.set_discard()
        card = self.g["Swashbuckler"].remove()
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.assertEqual(self.plr.get_coffers(), 0)

    def test_play_no_discard_coffers(self):
        """Player shouldn't get the Treasure Chest if they have no discards"""
        self.plr.set_coffers(4)
        self.plr.set_discard()
        card = self.g["Swashbuckler"].remove()
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.assertEqual(self.plr.get_coffers(), 4)
        self.assertFalse(self.plr.has_artifact("Treasure Chest"))

    def test_play_discard(self):
        self.plr.set_coffers(0)
        self.plr.set_discard("Copper")
        card = self.g["Swashbuckler"].remove()
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.assertEqual(self.plr.get_coffers(), 1)

    def test_play_coffers(self):
        self.plr.set_coffers(3)
        self.plr.set_discard("Copper")
        card = self.g["Swashbuckler"].remove()
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.assertIsNotNone(self.plr.has_artifact("Treasure Chest"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
