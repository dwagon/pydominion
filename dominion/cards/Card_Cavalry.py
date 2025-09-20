#!/usr/bin/env python

import unittest

from dominion import Card, Player, Game, Piles, Phase, OptionKeys, NoCardException


###############################################################################
class Card_Cavalry(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Cavalry"
        self.cost = 4
        self.required_cards = [("Card", "Horse")]

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.ACTION:
            return "Gain 2 Horses."
        return """Gain 2 Horses. When you gain this, +2 Cards, +1 Buy,
            and if it's your Buy phase return to your Action phase."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Horse")
            player.gain_card("Horse")
        except NoCardException:
            player.output("No more Horses")

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        if player.phase == Phase.BUY:
            player.phase = Phase.ACTION
        player.pickup_cards(2)
        player.buys.add(1)
        return {}


###############################################################################
class TestCavalry(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Cavalry"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Cavalry")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])

    def test_gain(self) -> None:
        self.plr.phase = Phase.BUY
        self.plr.gain_card("Cavalry")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(self.plr.phase, Phase.ACTION)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
