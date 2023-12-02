#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Caravan_Guard"""

import unittest
from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_CaravanGuard(Card.Card):
    """Caravan Guard"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Card, +1 Action. At the start of your next turn, +1 Coin.
            When another player plays an Attack card, you may play this from
            your hand. (+1 Action has no effect if it's not your turn.)"""
        self.name = "Caravan Guard"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.add_actions(1)
        player.pickup_cards(1)

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.coins.add(1)
        return {}

    def hook_under_attack(
        self, game: Game.Game, player: Player.Player, attacker: Player.Player
    ) -> None:
        player.output(f"Under attack from {attacker}")
        player.pickup_cards(1)
        player.move_card(player.piles[Piles.HAND]["Caravan Guard"], "played")


###############################################################################
class Test_CaravanGuard(unittest.TestCase):
    """Test Caravan Guard"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, initcards=["Caravan Guard", "Militia", "Moat"]
        )
        self.g.start_game()
        self.plr, self.attacker = self.g.player_list()
        self.card = self.g.get_card_from_pile("Caravan Guard")
        self.militia = self.g.get_card_from_pile("Militia")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Test playing the caravan guard"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)

    def test_attack(self) -> None:
        """Test being attacked"""
        self.plr.piles[Piles.HAND].set("Caravan Guard", "Moat")
        self.attacker.add_card(self.militia, Piles.HAND)
        self.attacker.play_card(self.militia)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertIn("Caravan Guard", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
