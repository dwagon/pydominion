#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Blockade"""

import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Blockade(Card.Card):
    """Blockade"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Gain a card costing up to $4, setting it aside.
At the start of your next turn, put it into your hand. While it's set aside, when another player
gains a copy of it on their turn, they gain a Curse."""
        self.name = "Blockade"
        self.cost = 4
        self.required_cards = ["Curse"]
        self._blockade: Optional[Card.Card] = None

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain a card costing up to $4, setting it aside."""
        self._blockade = player.plr_gain_card(4)
        assert self._blockade is not None
        player.move_card(self._blockade, Piles.DISCARD)  # In case it isn't there yet
        player.piles[Piles.DISCARD].remove(self._blockade)
        player.secret_count += 1

    def duration(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, str]]:
        """At the start of your next turn, put it into your hand"""
        if self._blockade:
            player.add_card(self._blockade, Piles.HAND)
            self._blockade = None
            player.secret_count -= 1
        return None

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> Optional[dict[OptionKeys, Any]]:
        """While it's set aside, when another player gains a copy of it on their turn, they gain a Curse."""
        if not self._blockade or player == owner:
            return None
        if card.name != self._blockade.name:
            return None
        try:
            player.output(f"Gained a Curse from {owner}'s Blockade")
            player.gain_card("Curse")
        except NoCardException:
            player.output("No more Curses")
        return None


###############################################################################
class TestBlockade(unittest.TestCase):
    """Test Blockade"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Blockade", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Blockade")

    def test_play_card(self) -> None:
        """Play the card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Silver -"]
        self.plr.play_card(self.card)
        self.assertIn("Blockade", self.plr.piles[Piles.DURATION])
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIsNotNone(self.card._blockade)
        self.vic.gain_card("Silver")
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIsNone(self.card._blockade)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
