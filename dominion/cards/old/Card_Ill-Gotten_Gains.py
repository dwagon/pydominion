#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, Phase, NoCardException, OptionKeys


###############################################################################
class Card_IGG(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.HINTERLANDS
        self.required_cards = ["Curse"]
        self.name = "Ill-Gotten Gains"
        self.cost = 5
        self.coin = 1

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """+1 Coin. When you play this, you may gain a Copper, putting
                it into your hand. When you gain this, each other player gains
                a Curse."""
        return "+1 Coin. When you play this, you may gain a Copper, putting it into your hand."

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.plr_choose_options(
            "Gain a Copper into your hand?",
            ("No thanks", False),
            ("Gain Copper", True),
        ):
            try:
                player.gain_card("Copper", destination=Piles.HAND)
            except NoCardException:
                player.output("No more Coppers")

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, Any]]:
        for plr in player.attack_victims():
            try:
                plr.gain_card("Curse")
                plr.output(f"Cursed because {player} gained an Ill-Gotten Gains")
            except NoCardException:
                player.output("No more Curses")
        return {}


###############################################################################
class TestIGG(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, oldcards=True, initcards=["Ill-Gotten Gains"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Ill-Gotten Gains")

    def test_play(self) -> None:
        """Play an Ill-Gotten Gains"""
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["copper"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.coins.get(), 1)

    def test_gain(self):
        """Gain an Ill-Gotten Gains"""
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.gain_card("Ill-Gotten Gains")
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
