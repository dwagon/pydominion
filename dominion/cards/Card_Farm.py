#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Farm"""
import unittest
from dominion import Card, Game, Piles, Player, Phase


###############################################################################
class Card_Farm(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.INTRIGUE
        self.name = "Farm"
        self.coin = 2
        self.victory = 2
        self.cost = 6

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+2 coin; 2 VPs"
        return "+2 coin"


###############################################################################
class Test_Farm(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Farm"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Farm")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Farm"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_score(self) -> None:
        """Score the Farm"""
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Farm"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
