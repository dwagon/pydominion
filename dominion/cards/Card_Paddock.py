#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Paddock"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Paddock(Card.Card):
    """Paddock"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+2 Coin; Gain 2 Horses. +1 Action per empty Supply pile."""
        self.name = "Paddock"
        self.coin = 2
        self.cost = 5
        self.required_cards = [("Card", "Horse")]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Horse")
            player.gain_card("Horse")
        except NoCardException:
            player.output("No more Horses")
        empties = sum(1 for _, st in game.get_card_piles() if st.is_empty())
        player.add_actions(empties)


###############################################################################
class TestPaddock(unittest.TestCase):
    """Test Paddock"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Paddock", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Paddock")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card_one_stack(self) -> None:
        while True:
            try:
                self.g.get_card_from_pile("Moat")
            except NoCardException:
                break
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
