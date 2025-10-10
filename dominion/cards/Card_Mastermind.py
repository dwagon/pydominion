#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Mastermind"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Mastermind(Card.Card):
    """Mastermind"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """At the start of your next turn, you may play an Action card from your hand three times."""
        self.name = "Mastermind"
        self.cost = 5

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        choices: list[tuple[str, Any]] = [("Don't play a card", None)]
        for card in player.piles[Piles.HAND]:
            if not card.isAction():
                continue
            choices.append((f"Play {card} thrice", card))
        if len(choices) == 1:
            player.output("No action cards to repeat")
            return {}
        if card := player.plr_choose_options("Play which action card three times?", *choices):
            for i in range(1, 4):
                player.output(f"Number {i} play of {card}")
                player.play_card(card, discard=False, cost_action=False)
            if card.location == Piles.HAND:
                player.move_card(card, Piles.PLAYED)
        return {}


###############################################################################
class TestMastermind(unittest.TestCase):
    """Test Mastermind"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Mastermind", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mastermind")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a card"""
        self.plr.piles[Piles.DISCARD].set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Play Moat"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
