#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException, PlayArea


###############################################################################
class Card_TreasureHunter(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action, +1 Coin; Gain a Silver per card the player
            to your right gained in his last turn. Discard to replace with Warrior"""
        self.name = "Treasure Hunter"
        self.purchasable = False
        self.actions = 1
        self.coin = 1
        self.cost = 3
        self.numcards = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain a Silver per card the player to your right gained in his last turn"""
        righty = game.playerToRight(player)
        num_silver = len(righty.stats["gained"])
        player.output(
            f"Gaining {num_silver} silvers as {righty} gained {num_silver} cards"
        )
        for _ in range(num_silver):
            try:
                player.gain_card("Silver")
            except NoCardException:  # pragma: no coverage
                player.output("No more Silvers")

    def hook_discard_this_card(
        self, game: Game.Game, player: Player.Player, source: PlayArea.PlayArea
    ) -> None:
        """Replace with Warrior"""
        player.replace_traveller(self, "Warrior")


###############################################################################
class TestTreasureHunter(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Page"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Treasure Hunter")

    def test_treasure_hunter(self) -> None:
        """Play a treasure_hunter"""
        self.other.gain_card("Copper")
        self.other.gain_card("Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
