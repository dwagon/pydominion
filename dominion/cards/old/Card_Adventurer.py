#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Adventurer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Dig through deck for two treasures"
        self.name = "Adventurer"
        self.cost = 6

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal cards from your deck until you reveal two treasure cards
        Add those to your hand and discard the other revealed cards"""
        treasures: list[Card.Card] = []
        while len(treasures) < 2:
            try:
                card = player.pickup_card(verbose=False)
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isTreasure():
                treasures.append(card)
                player.output(f"Adding {card}")
            else:
                player.discard_card(card)
                player.output(f"Discarding {card} as not treasure")


###############################################################################
class Test_Adventurer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Adventurer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_treasures(self) -> None:
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Estate")
        self.plr.piles[Piles.HAND].set("Adventurer")
        self.plr.play_card(self.plr.piles[Piles.HAND].top_card())
        self.assertEqual(
            sorted(["Silver", "Gold"]),
            sorted([_.name for _ in self.plr.piles[Piles.HAND]]),
        )
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Estate"])
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
