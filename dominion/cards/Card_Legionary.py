#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Legionary"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Legionary(Card.Card):
    """Legionary"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+3 Coin. You may reveal a Gold from your hand.
            If you do, each other player discards down to 2 cards in hand, then draws a card."""
        self.name = "Legionary"
        self.cost = 5
        self.coin = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if au := player.piles[Piles.HAND]["Gold"]:
            player.reveal_card(au)
            for plr in player.attack_victims():
                plr.output(f"{player.name}'s Legionary forces you to discard down to 2")
                plr.plr_discard_down_to(2)
                plr.pickup_cards(1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    """Discard down to 2"""
    num_to_discard = len(player.piles[Piles.HAND]) - 2
    return player.pick_to_discard(num_to_discard)


###############################################################################
class TestLegionary(unittest.TestCase):
    """Test Legionary"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Legionary"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Legionary")

    def test_play(self):
        """Play a Legionary"""
        self.plr.piles[Piles.HAND].set("Gold")
        self.victim.test_input = ["1", "2", "3", "0"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
