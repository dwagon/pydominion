#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sleigh"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, OptionKeys, Player, NoCardException


###############################################################################
class Card_Sleigh(Card.Card):
    """Sleigh"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain 2 Horses. When you gain a card, you may discard this,
            to put that card into your hand or onto your deck."""
        self.name = "Sleigh"
        self.cost = 2
        self.required_cards = [("Card", "Horse")]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Horse")
            player.gain_card("Horse")
        except NoCardException:
            player.output("No more Horses")

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        # Discard self if choice == hand or deck
        choice = player.plr_choose_options(
            f"What to do with {card}?",
            ("Discard by default", Piles.DISCARD),
            (f"Put {card} into hand and discard Sleigh", Piles.HAND),
            (f"Put {card} onto your deck and discard Sleigh", Piles.TOPDECK),
        )
        if choice == Piles.DISCARD:
            return {}
        if self in player.piles[Piles.PLAYED]:
            player.piles[Piles.PLAYED].remove(self)
        elif self in player.piles[Piles.HAND]:
            player.piles[Piles.HAND].remove(self)
        player.discard_card(self)
        return {OptionKeys.DESTINATION: choice}


###############################################################################
class TestSleigh(unittest.TestCase):
    """Test Sleigh"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sleigh"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.plr.get_card_from_pile("Sleigh")
        self.g.card_piles["Horse"].set_debug()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_sleigh(self) -> None:
        """Play a sleigh"""
        self.plr.test_input = ["Discard by default", "Put Horse into hand"]
        self.plr.play_card(self.card)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])
        self.assertIn("Horse", self.plr.piles[Piles.HAND])

    def test_gain_card(self) -> None:
        """Gain a card while Sleigh in hand"""
        self.plr.test_input = ["Put Estate onto your deck"]
        self.plr.gain_card("Estate")
        self.assertIn("Estate", self.plr.piles[Piles.DECK])
        self.assertIn("Sleigh", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
