#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Loan """

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


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
        max_count = player.count_cards()
        count = 0
        treasure = None
        while True:
            count += 1
            if count > max_count:
                player.output("No treasures")
                break
            try:
                card = player.next_card()
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isTreasure():
                treasure = card
                break
            player.output(f"Revealed and discarded {card}")
            player.discard_card(card)
        if not treasure:
            return
        if player.plr_choose_options(
            "What to do?", (f"Discard {treasure}", True), (f"Trash {treasure}", False)
        ):
            player.discard_card(treasure)
        else:
            player.trash_card(treasure)


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

    def test_no_treasures(self) -> None:
        self.plr.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.loan = self.plr.gain_card("Loan", Piles.HAND)
        self.plr.play_card(self.loan)
        self.assertIn("No treasures", self.plr.messages)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
