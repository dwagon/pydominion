#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Monkey """

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Monkey(Card.Card):
    """Monkey"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Until your next turn, when the player to your right gains a card,
            +1 Card.  At the start of your next turn, +1 Card."""
        self.name = "Monkey"
        self.cost = 3

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """Until your next turn, when the player to your right gains a card, +1 Card"""
        if player == game.playerToRight(owner):
            owner.pickup_cards(1)
        return {}

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        """At the start of your next turn, +1 Card."""
        player.pickup_cards(1)
        return {}


###############################################################################
class Test_Monkey(unittest.TestCase):
    """Test Monkey"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Monkey", "Moat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Monkey")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play Monkey"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.oth.gain_card("Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
