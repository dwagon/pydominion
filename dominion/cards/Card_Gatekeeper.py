#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Gatekeeper"""

import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Gatekeeper(Card.Card):
    """Gatekeeper"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """ At the start of your next turn, +$3. Until then, when another player
        gains an Action or Treasure card they don't have an Exiled copy of, they Exile it."""
        self.name = "Gatekeeper"
        self.cost = 5

    def duration(self, game: Game.Game, player: Player.Player) -> None:
        player.coins.add(3)

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> Optional[dict[OptionKeys, Any]]:
        if player == owner:
            return None
        if (card.isAction() or card.isTreasure()) and card.name not in player.piles[
            Piles.EXILE
        ]:
            player.output(f"{owner}'s Gatekeeper exiles your {card}")
            player.exile_card(card)
            return {OptionKeys.DONTADD: True}
        return None


###############################################################################
class TestGatekeeper(unittest.TestCase):
    """Test Gatekeeper"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Gatekeeper"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Gatekeeper")

    def test_play_card(self) -> None:
        """Play the card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 3)

    def test_attack(self) -> None:
        """Test the attack where there is no exile"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.victim.gain_card("Gold")
        self.assertIn("Gold", self.victim.piles[Piles.EXILE])
        self.assertNotIn("Gold", self.victim.piles[Piles.DISCARD])

    def test_attack_exile(self) -> None:
        """Test the attack where there is already an exile"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.victim.test_input = ["Do nothing"]
        self.victim.piles[Piles.EXILE].set("Gold")
        self.victim.gain_card("Gold")
        self.assertIn("Gold", self.victim.piles[Piles.EXILE])
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
