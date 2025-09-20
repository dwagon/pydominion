#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Marauder"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Marauder(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.LOOTER,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = (
            "Gain a Spoils from the Spoils pile. Each other player gains a Ruins."
        )
        self.name = "Marauder"
        self.cost = 4
        self.required_cards = ["Spoils"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            try:
                victim.gain_card("Ruins")
                victim.output(f"Gained a ruin from {player}'s Marauder")
            except NoCardException:
                player.output("No more Ruins")
        try:
            player.gain_card("Spoils")
        except NoCardException:
            player.output("No more Spoils")


###############################################################################
class TestMarauder(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Marauder"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Marauder")

    def test_play(self) -> None:
        """Play a marauder"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Spoils", self.plr.piles[Piles.DISCARD])
        self.g.print_state()
        self.assertTrue(self.victim.piles[Piles.DISCARD][0].isRuin())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
