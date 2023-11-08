#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Harvest(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """Reveal the top 4 cards of your deck, then discard them. Coin per differently named card revealed."""
        self.name = "Harvest"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards = set()
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:
                continue
            player.reveal_card(card)
            cards.add(card.name)
            player.output(f"Revealed a {card}")
            player.add_card(card, Piles.DISCARD)
        player.output(f"Gaining {len(cards)} coins")
        player.coins.add(len(cards))


###############################################################################
class Test_Harvest(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Harvest"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Harvest")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Harvest"""
        self.plr.piles[Piles.DECK].set("Duchy", "Duchy", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Duchy", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
