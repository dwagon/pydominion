#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Siren"""

import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, Phase, NoCardException, OptionKeys


###############################################################################
class Card_Siren(Card.Card):
    """Siren"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.name = "Siren"
        self.cost = 3
        self.required_cards = ["Curse"]

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """Each other player gains a Curse. 
            At the start of your next turn, draw until you have 8 cards in hand.
            When you gain this, trash it unless you trash an Action from your hand."""
        return """Each other player gains a Curse. 
        At the start of your next turn, draw until you have 8 cards in hand."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player gains a Curse."""
        for victim in player.attack_victims():
            try:
                victim.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")

    def duration(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, str]]:
        """At the start of your next turn, draw until you have 8 cards in hand."""
        while player.piles[Piles.HAND].size() < 8:
            try:
                player.pickup_card()
            except NoCardException:
                break
        return None

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, Any]]:
        """When you gain this, trash it unless you trash an Action from your hand."""
        if actions := [_ for _ in player.piles[Piles.HAND] if _.isAction()]:
            if player.plr_trash_card(
                num=1,
                prompt="Either trash an action or trash the Siren",
                cardsrc=actions,
            ):
                return None
        player.output("Trashing Siren as no Action card was trashed")
        return {OptionKeys.TRASH: True}


###############################################################################
class TestSiren(unittest.TestCase):
    """Test Siren"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Siren", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Siren")

    def test_gain_card_no_action(self) -> None:
        """Gain a card with no action"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.gain_card("Siren")
        self.assertIn("Siren", self.g.trash_pile)
        self.assertNotIn("Siren", self.plr.piles[Piles.DISCARD])

    def test_gain_card_with_action(self) -> None:
        """Gain a card with an action"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Moat")
        self.plr.test_input = ["Trash Moat"]
        self.plr.gain_card("Siren")
        self.assertIn("Moat", self.g.trash_pile)
        self.assertIn("Siren", self.plr.piles[Piles.DISCARD])

    def test_play_card(self) -> None:
        """Play the siren"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
