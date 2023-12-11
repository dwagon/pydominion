#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Trickster"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys, PlayArea


###############################################################################
class Card_Trickster(Card.Card):
    """Trickster"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Each other player gains a Curse. Once this turn, when you discard a Treasure from play,
        you may set it aside. Put it in your hand at end of turn."""
        self.name = "Trickster"
        self.cost = 5
        self.set_aside = PlayArea.PlayArea()
        self.required_cards = ["Curse"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            try:
                victim.gain_card("Curse")
                victim.output(f"{player}'s Trickster curses you")
            except NoCardException:  # pragma: no coverage
                player.output("No more Curses")

    def hook_discard_any_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        """Once this turn, when you discard a Treasure from play,
        you may set it aside."""
        if not card.isTreasure() or self.location not in Piles.PLAYED:
            return {}
        if not self.set_aside:
            options = [(f"Set {card} aside", True), ("Discard as normal", False)]
            if player.plr_choose_options(
                "Set treasure aside to put in hand at end of turn?", *options
            ):
                player.move_card(card, self.set_aside)
        return {}

    def hook_end_turn(self, game: Game.Game, player: Player.Player) -> None:
        """Put it in your hand at end of turn."""
        if self.set_aside:
            card = self.set_aside.next_card()
            player.output(f"Putting {card} back in hand from Trickster")
            player.add_card(card, Piles.HAND)


###############################################################################
class TestTrickster(unittest.TestCase):
    """Test Trickster"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Trickster", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Trickster")

    def test_play_card(self) -> None:
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.plr.test_input = ["Set Silver"]
        self.plr.discard_card(self.plr.piles[Piles.HAND]["Silver"])
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])
        self.plr.end_turn()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
