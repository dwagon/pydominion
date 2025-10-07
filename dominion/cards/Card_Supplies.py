#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Supplies"""

import unittest

from dominion import Game, Piles, NoCardException, Player, Card


###############################################################################
class Card_Supplies(Card.Card):
    """Supplies"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 coin; When you play this, gain a Horse onto your deck."
        self.name = "Supplies"
        self.coin = 1
        self.cost = 2
        self.required_cards = [("Card", "Horse")]

    def special(self, game: Game.Game, player: Player.Player):
        try:
            player.gain_card("Horse", Piles.TOPDECK)
        except NoCardException:
            player.output("No more Horses")


###############################################################################
class TestSupplies(unittest.TestCase):
    """Test Supplies"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Supplies"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Supplies")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a supplies"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Horse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
