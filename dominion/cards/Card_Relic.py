#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Relic"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Relic(Card.Card):
    """Relic"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+2 Coin; Each other player gains a -1 Card token"
        self.name = "Relic"
        self.coin = 2
        self.cost = 5

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """When you play this, each other player puts his -1 Card token
        on his deck."""
        for victim in player.attack_victims():
            victim.card_token = True
            victim.output(f"-1 Card token active due to Relic by {player}")


###############################################################################
class TestRelic(unittest.TestCase):
    """Test Relic"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Relic"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Relic")

    def test_play(self):
        """Play a relic"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertTrue(self.victim.card_token)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
