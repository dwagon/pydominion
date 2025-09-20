#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Distant_Shore"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Distant_Shore(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.VICTORY,
            Card.CardType.ODYSSEY,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.name = "Distant Shore"
        self.cards = 2
        self.actions = 1
        self.victory = 2
        self.desc = """ +2 Cards; +1 Action; Gain an Estate. 2VP"""
        self.pile = "Odysseys"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Estate")
        except NoCardException:  # pragma: no coverage
            player.output("No more Estates")


###############################################################################
class Test_Distant_Shore(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Odysseys", "Distant Shore")

    def test_play(self) -> None:
        """Play the card"""
        hand_size = self.plr.piles[Piles.HAND].size()
        actions = self.plr.actions.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hand_size + 2)
        self.assertEqual(self.plr.actions.get(), actions)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.get_score_details()["Distant Shore"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
