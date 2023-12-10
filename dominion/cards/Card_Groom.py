#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Groom """


import contextlib
import unittest
from dominion import Game, Card, Piles, NoCardException, Player


###############################################################################
class Card_Groom(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.cost = 4
        self.name = "Groom"
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain a card costing up to 4 Coin. If it's an...
            Action card, gain a Horse;
            Treasure card, gain a Silver;
            Victory card, +1 Card and +1 Action."""
        self.required_cards = [("Card", "Horse")]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        card = player.plr_gain_card(4)
        if card is None:
            return
        if card.isAction():
            try:
                player.gain_card("Horse")
                player.output("Gained a Horse")
            except NoCardException:
                player.output("No more Horses")
        if card.isTreasure():
            try:
                player.gain_card("Silver")
                player.output("Gained a Silver")
            except NoCardException:
                player.output("No more Silver")
        if card.isVictory():
            with contextlib.suppress(NoCardException):
                player.pickup_card()
            player.add_actions(1)


###############################################################################
class Test_Groom(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Groom", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Groom")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card_action(self) -> None:
        """Play Card"""
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])

    def test_play_card_victory(self) -> None:
        """Play Card"""
        self.plr.test_input = ["Get Estate"]
        self.plr.play_card(self.card)
        self.assertNotIn("Horse", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
