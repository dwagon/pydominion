#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Vassal(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.name = "Vassal"
        self.coin = 2
        self.cost = 3
        self.desc = "+2 Coin; Discard the top card of your deck. If it is an Action card, you may play it."

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            card = player.next_card()
        except NoCardException:
            return
        player.reveal_card(card)
        if card.isAction():
            player.add_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)
        else:
            player.add_card(card, Piles.DISCARD)


###############################################################################
class Test_Vassal(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Vassal", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Vassal")

    def test_play_action(self) -> None:
        """Play a Vassal with action next"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_play_non_action(self) -> None:
        """Play a Vassal with non-action next"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
