#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Patron"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Patron(Card.Card):
    """Patron"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "+1 Villager; +2 Coin. When something causes you to reveal this, +1 Coffers."
        self.name = "Patron"
        self.cost = 4
        self.coin = 2

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.villagers.add(1)

    def hook_reveal_this_card(self, game: "Game.Game", player: "Player.Player") -> None:
        player.coffers.add(1)


###############################################################################
class TestPatron(unittest.TestCase):
    """Test Patron"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Patron"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Patron")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.villagers.get(), 1)

    def test_reveal(self):
        num = self.plr.coffers.get()
        self.plr.reveal_card(self.card)
        self.assertEqual(self.plr.coffers.get(), num + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
