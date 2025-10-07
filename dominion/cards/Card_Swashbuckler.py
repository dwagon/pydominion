#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Swashbuckler"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Swashbuckler(Card.Card):
    """Swashbuckler"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+3 Cards. If your discard pile has any cards in it:
            +1 Coffers, then if you have at least 4 Coffers tokens, take the
            Treasure Chest."""
        self.name = "Swashbuckler"
        self.needsartifacts = True
        self.cards = 3
        self.cost = 5

    ###########################################################################
    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.piles[Piles.DISCARD].size() >= 1:
            player.output("Gained a coffer")
            player.coffers.add(1)
            if player.coffers.get() >= 4:
                if not player.has_artifact("Treasure Chest"):
                    player.output("Gained the Treasure Chest")
                    player.assign_artifact("Treasure Chest")


###############################################################################
class TestSwashbuckler(unittest.TestCase):
    """Test Swashbuckler"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Swashbuckler"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Swashbuckler")

    def test_play_no_discard(self):
        self.plr.coffers.set(0)
        self.plr.piles[Piles.DISCARD].set()
        card = self.g.get_card_from_pile("Swashbuckler")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.coffers.get(), 0)

    def test_play_no_discard_coffers(self):
        """Player shouldn't get the Treasure Chest if they have no discards"""
        self.plr.coffers.set(4)
        self.plr.piles[Piles.DISCARD].set()
        card = self.g.get_card_from_pile("Swashbuckler")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.coffers.get(), 4)
        self.assertFalse(self.plr.has_artifact("Treasure Chest"))

    def test_play_discard(self):
        self.plr.coffers.set(0)
        self.plr.piles[Piles.DISCARD].set("Copper")
        card = self.g.get_card_from_pile("Swashbuckler")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.coffers.get(), 1)

    def test_play_coffers(self):
        self.plr.coffers.set(3)
        self.plr.piles[Piles.DISCARD].set("Copper")
        card = self.g.get_card_from_pile("Swashbuckler")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertIsNotNone(self.plr.has_artifact("Treasure Chest"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
