#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player

FOOL = "fool"


###############################################################################
class Card_Fool(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """If you aren't the player with Lost in the Woods, take it, take 3 Boons, 
        and receive the Boons in any order."""
        self.name = "Fool"
        self.cost = 3
        self.heirloom = "Lucky Coin"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.has_state("Lost in the Woods"):
            return
        player.assign_state("Lost in the Woods")
        player.specials[FOOL] = True  # For testing
        for _ in range(3):
            player.receive_boon()


###############################################################################
class TestFool(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Fool"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fool")
        self.plr.specials[FOOL] = False

    def test_play_with(self) -> None:
        """Play a Fool with Lost in the Woods"""
        self.plr.assign_state("Lost in the Woods")
        self.plr.specials[FOOL] = False
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertFalse(self.plr.specials[FOOL])

    def test_play_without(self) -> None:
        """Play a Fool without Lost in the Woods"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.specials[FOOL] = False
        self.plr.test_input = ["Finish", "Finish", "Finish"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.specials[FOOL])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
