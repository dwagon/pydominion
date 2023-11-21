#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Warlord """

import unittest
from collections import Counter
from typing import Optional, Any

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_Warlord(Card.Card):
    """Warlord"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.CLASH,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.pile = "Clashes"
        self.name = "Warlord"
        self.actions = 1
        self.desc = """+1 Action; At the start of your next turn, +2 Cards.
            Until then, other players can't play an Action from their hand that
            they have 2 or more copies of in play."""

    def hook_all_players_pre_play(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> Optional[dict[OptionKeys, Any]]:
        """Until then, other players can't play an Action from their hand that
        they have 2 or more copies of in play."""
        if not card.isAction():
            return {}
        counter = Counter()
        for crd in player.piles[Piles.PLAYED]:
            counter += Counter([crd.name])
        if counter[card.name] >= 2:
            player.output(
                f"{owner}'s Warlord prevents you playing {card} more than twice"
            )
            return {OptionKeys.SKIP_CARD: True}
        return {}

    def duration(self, game: Game.Game, player: Player.Player) -> None:
        """At the start of your next turn, +2 Cards."""
        player.pickup_cards(num=2)


###############################################################################
class TestWarlord(unittest.TestCase):
    """Test Warlord"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, initcards=["Clashes", "Militia"], use_liaisons=True
        )
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()

    def test_play(self) -> None:
        """Play Card"""
        card = self.g.get_card_from_pile("Clashes", "Warlord")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_others_playing(self) -> None:
        """Other players playing actions"""
        card = self.g.get_card_from_pile("Clashes", "Warlord")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        mil = self.g.get_card_from_pile("Militia")
        self.oth.add_card(mil, Piles.HAND)
        self.oth.piles[Piles.PLAYED].set("Militia", "Militia", "Copper")
        self.oth.play_card(mil)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
