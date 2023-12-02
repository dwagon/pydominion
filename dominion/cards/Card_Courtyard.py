#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Courtyard(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+3 cards. Put a card from your hand on top of your deck."
        self.name = "Courtyard"
        self.cards = 3
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Put a card from your hand on top of your deck"""
        cards = player.card_sel(
            prompt="Put which card on top of deck?", num=1, verbs=("Put", "Unput")
        )
        if not cards:
            return
        card = cards[0]
        player.move_card(card, "topdeck")
        player.output(f"Put {card} on top of deck")


###############################################################################
class Test_Courtyard(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Courtyard"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.cy = self.g.get_card_from_pile("Courtyard")

    def test_play(self) -> None:
        """Play courtyard"""
        self.plr.add_card(self.cy, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.cy)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)

    def test_put_card(self) -> None:
        """Use courtyard to put a card to the top of the deck"""
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.cy, Piles.HAND)
        self.plr.test_input = ["put gold"]
        self.plr.play_card(self.cy)
        card = self.plr.next_card()
        self.assertEqual(card.name, "Gold")
        for c in self.plr.piles[Piles.HAND]:
            self.assertNotEqual(c.name, "Gold")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
