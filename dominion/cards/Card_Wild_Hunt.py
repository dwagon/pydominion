#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_WildHunt(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.GATHERING]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Choose one: +3 Cards and add 1 VP to the Wild Hunt
            Supply pile; or gain an Estate, and if you do, take the VP from the pile."""
        self.name = "Wild Hunt"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.plr_choose_options(
            "Choose one:",
            ("+3 Cards and add 1 VP to the Wild Hunt Supply pile", True),
            (
                "Gain an Estate, and if you do, take %d VP from the pile."
                % game.card_piles["Wild Hunt"].getVP(),
                False,
            ),
        ):
            player.pickup_cards(3)
            game.card_piles["Wild Hunt"].addVP()
        else:
            try:
                player.gain_card("Estate")
            except NoCardException:
                player.output("No more Estates")
            score = game.card_piles["Wild Hunt"].drainVP()
            player.output(f"Gaining {score} VP from Wild Hunt")
            player.add_score("Wild Hunt", score)


###############################################################################
class Test_WildHunt(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wild Hunt"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wild Hunt")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_give(self) -> None:
        """Play a Wild Hunt and take the cards"""
        self.plr.test_input = ["Cards"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 3)
        self.assertEqual(self.g.card_piles["Wild Hunt"].getVP(), 1)

    def test_play_take(self) -> None:
        """Play a Wild Hunt and take the score"""
        self.plr.test_input = ["Gain"]
        self.g.card_piles["Wild Hunt"].addVP(3)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.get_score_details()["Wild Hunt"], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
