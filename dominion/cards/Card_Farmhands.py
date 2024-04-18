#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Farmhands"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Farmhands(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.name = "Farmhands"
        self.cost = 4
        self.cards = 1
        self.actions = 2
        self.desc = """+1 Card, +2 Actions. When you gain this, you may set aside an Action or Treasure from your hand,
        and play it at the start of your next turn."""

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        act_treas = [_ for _ in player.piles[Piles.HAND] if _.isAction() or _.isTreasure()]
        if not act_treas:  # pragma: no cover
            return {}
        options = [("Do nothing", None)]
        for card in act_treas:
            options.append((f"Play {card}", card))
        if choice := player.plr_choose_options("Pick a card to play next turn", *options):
            player.defer_card(choice)
        return {}


###############################################################################
class Test_Farmhands(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Farmhands"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Farmhands")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Farmhands"""
        actions = self.plr.actions.get()
        num_cards = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), num_cards + 1 - 1)

    def test_gain(self) -> None:
        """Play and set aside an action"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["Play Gold"]
        self.plr.gain_card("Farmhands")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
