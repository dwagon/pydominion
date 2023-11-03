#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_WilloWisp(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SPIRIT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+1 Card; +1 Action; Reveal the top card of your deck.
        If it costs 2 or less, put it into your hand."""
        self.name = "Will-o'-Wisp"
        self.purchasable = False
        self.cards = 1
        self.actions = 1
        self.insupply = False
        self.cost = 0

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        try:
            card = player.next_card()
        except NoCardException:
            return

        player.reveal_card(card)
        if card.cost <= 2 and not card.potcost and not card.debtcost:
            player.add_card(card, Piles.HAND)
            player.output(f"Moving {card} from your deck to your hand")
        else:
            player.add_card(card, "topdeck")
            player.output(f"Keep {card} on top of your deck")


###############################################################################
class TestWilloWisp(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Will-o'-Wisp"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Will-o'-Wisp")

    def test_special_cheap(self) -> None:
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])

    def test_special_expensive(self) -> None:
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
