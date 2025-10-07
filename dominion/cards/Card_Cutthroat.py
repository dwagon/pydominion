#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Cutthroat"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Cutthroat(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Each other player discards down to 3 cards in hand.
The next time anyone gains a Treasure costing $5 or more, gain a Loot."""
        self.name = "Cutthroat"
        self.cost = 5
        self.required_cards = ["Loot"]
        self.permanent = True

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player discards down to 3 cards in hand."""
        for plr in player.attack_victims():
            plr.output(f"{player}'s Cutthroat: Discard down to 3 cards")
            plr.plr_discard_down_to(3)

    ###########################################################################
    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """The next time anyone gains a Treasure costing $5 or more, gain a Loot."""
        if self.location != Piles.DURATION:
            return {}
        if owner.card_cost(card) >= 5 and card.isTreasure():
            owner.move_card(self, Piles.DISCARD)  # Discard first to avoid recursion
            owner.output(f"Gained a Loot from Cutthroat as {player} gained a {card}")
            owner.gain_card("Loot")
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    num_to_discard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Cutthroat(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Cutthroat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cutthroat")

    def test_play(self) -> None:
        """Play Cutthroat"""
        self.plr.add_card(self.card, Piles.HAND)
        self.victim.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)  # Normal  - 2
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)

    def test_gain(self) -> None:
        """Someone gains a treasure"""
        self.plr.add_card(self.card, Piles.DURATION)
        self.victim.gain_card("Gold")
        found = any([True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
