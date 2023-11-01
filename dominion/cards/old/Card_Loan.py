#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Loan """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Loan(Card.Card):
    """Loan"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Coin; When you play this, reveal cards from your
            deck until you reveal a Treasure. Discard it or trash it. Discard
            the other cards."""
        self.name = "Loan"
        self.cost = 3
        self.coin = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """When you play this, reveal cards from your deck until
        you reveal a Treasure. Discard it or trash it. Discard the
        other cards"""
        while True:
            card = player.next_card()
            if card is None:
                break
            player.reveal_card(card)
            if card.isTreasure():
                break
            player.output(f"Revealed and discarded {card}")
            player.discard_card(card)
        discard = player.plr_choose_options(
            "What to do?", (f"Discard {card}", True), (f"Trash {card}", False)
        )
        if discard:
            player.discard_card(card)
        else:
            player.trash_card(card)


###############################################################################
class Test_Loan(unittest.TestCase):
    """Test Loan"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Loan"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.loan = self.plr.gain_card("Loan", Piles.HAND)

    def test_discard(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set("Estate", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Discard Gold"]
        self.plr.play_card(self.loan)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.g.trash_pile.size(), trash_size)

    def test_trash(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set("Estate", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Trash Gold"]
        self.plr.play_card(self.loan)
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
