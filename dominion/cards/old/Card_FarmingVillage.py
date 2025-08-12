#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_FarmingVillage(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+2 actions. Reveal cards from the top of your deck until
            you reveal an Action or Treasure card. Put that card into your hand
            and discard the other cards."""
        self.name = "Farming Village"
        self.actions = 2
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal cards from the top of your deck until you revel
        an Action or Treasure card. Put that card into your hand
        and discard the other cards."""
        while True:
            try:
                card = player.next_card()
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isTreasure() or card.isAction():
                player.output(f"Added {card} to hand")
                player.add_card(card, Piles.HAND)
                break
            player.output(f"Picked up and discarded {card}")
            player.discard_card(card)


###############################################################################
class TestFarmingVillage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Farming Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Farming Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_treasure(self) -> None:
        """Play farming village with a treasure in deck"""
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Silver", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Estate")

    def test_play_action(self) -> None:
        """Play farming village with an action in deck"""
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Farming Village", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertIn("Farming Village", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Estate")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
