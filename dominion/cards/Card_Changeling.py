#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Phase, OptionKeys, Player, NoCardException


###############################################################################
class Card_Changeling(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Trash this. Gain a copy of a card you have in play.
In games using this, when you gain a card costing 3 or more, you may exchange it for a Changeling."""
        self.name = "Changeling"
        self.cost = 3

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[OptionKeys, Any]]:
        if card.cost < 3:
            return None
        if game.card_piles["Changeling"].is_empty():
            return None
        if swap := player.plr_choose_options(
            f"Swap {card} for a Changeling?",
            (f"Swap {card}", True),
            (f"Keep {card}", False),
        ):
            return {OptionKeys.REPLACE: "Changeling"}
        return None

    def night(self, game: Game.Game, player: Player.Player) -> None:
        options = [{"selector": "0", "print": "Keep Changeling", "card": None}]
        index = 1
        for card in player.piles[Piles.PLAYED] + player.piles[Piles.HAND]:
            pr = f"Exchange for {card}"
            options.append({"selector": f"{index}", "print": pr, "card": card})
            index += 1
        o = player.user_input(options, "Trash Changeling to gain a card")
        if o["card"]:
            player.trash_card(self)
            try:
                player.gain_card(o["card"].name)
            except NoCardException:
                player.output(f"No more {o['card']}")


###############################################################################
class TestChangeling(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Changeling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Changeling")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_keep(self) -> None:
        self.plr.phase = Phase.NIGHT
        self.plr.test_input = ["Keep Changeling"]
        self.plr.play_card(self.card)
        self.assertIn("Changeling", self.plr.piles[Piles.PLAYED])

    def test_play_swap(self) -> None:
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.PLAYED].set("Gold")
        self.plr.test_input = ["Exchange for Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Changeling", self.g.trash_pile)

    def test_gain_keep(self) -> None:
        self.plr.test_input = ["Keep Silver"]
        self.plr.gain_card("Silver")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_gain_swap(self) -> None:
        self.plr.test_input = ["Swap Silver"]
        self.plr.gain_card("Silver")
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Changeling", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
