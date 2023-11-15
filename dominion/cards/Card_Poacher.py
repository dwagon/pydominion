#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Poacher """

import unittest
from dominion import Card, Game, Piles, NoCardException, Player


###############################################################################
class Card_Poacher(Card.Card):
    """Poacher"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+1 Card, +1 Action, +1 Coin. Discard a card per empty supply pile."
        self.name = "Poacher"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        empties = sum(1 for _, st in game.get_card_piles() if st.is_empty())
        if empties:
            player.plr_discard_cards(num=empties, force=True)


###############################################################################
class TestPoacher(unittest.TestCase):
    """Test Poacher"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Poacher", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Poacher")

    def test_play(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_empty(self) -> None:
        """Play card with an empty pile"""
        self.plr.piles[Piles.HAND].set("Gold", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        while True:
            try:
                self.g.get_card_from_pile("Moat")
            except NoCardException:
                break
        self.plr.test_input = ["Discard Gold"]
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
