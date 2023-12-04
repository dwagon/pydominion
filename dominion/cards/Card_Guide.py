#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Guide(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Card, +1 Action; Call to discard hand and draw 5"
        self.name = "Guide"
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def hook_call_reserve(self, game: Game.Game, player: Player.Player) -> None:
        player.output("Discarding current hand and picking up 5 new cards")
        player.discard_hand()
        player.pickup_cards(5)


###############################################################################
class Test_Guide(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Guide"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Guide")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_call(self) -> None:
        """Call Guide from reserve"""
        self.plr.piles[Piles.HAND].set("Estate", "Estate")
        self.plr.piles[Piles.DECK].set(
            "Copper", "Copper", "Copper", "Copper", "Copper", "Copper"
        )
        self.plr.piles[Piles.RESERVE].set("Guide")
        self.plr.call_reserve("Guide")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertNotIn("Estate", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
