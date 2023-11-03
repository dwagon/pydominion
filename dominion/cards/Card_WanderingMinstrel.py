#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_WanderingMinstrel(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card, +2 Actions. Reveal the top 3 cards of your deck.
            Put the Actions back on top in any order and discard the rest."""
        self.name = "Wandering Minstrel"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        cards = []
        for _ in range(3):
            try:
                card = player.next_card()
            except NoCardException:
                continue
            player.reveal_card(card)
            if card.isAction():
                cards.append(card)
                player.output(f"Revealed a {card} and put on top of deck")
            else:
                player.add_card(card, "discard")
                player.output(f"Discarded {card}")

        for card in cards:
            player.add_card(card, "topdeck")


###############################################################################
class TestWanderingMinstrel(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wandering Minstrel", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wandering Minstrel")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Wandering Minstrel"""
        self.plr.piles[Piles.DECK].set("Duchy", "Moat", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertIn("Moat", self.plr.piles[Piles.DECK])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
