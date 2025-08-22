#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, OptionKeys, Player, Phase


###############################################################################
class Card_NomadCamp(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.name = "Nomad Camp"
        self.buys = 1
        self.cards = 2
        self.cost = 4

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.ACTION:
            return "+1 Buy +2 Coins"
        return "+1 Buy +2 Coins; When you gain this, put it on top of your deck."

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        return {OptionKeys.DESTINATION: Piles.TOPDECK}


###############################################################################
class Test_NomadCamp(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Nomad Camp"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Nomad Camp")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_gain(self) -> None:
        self.plr.gain_card("Nomad Camp")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Nomad Camp")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
