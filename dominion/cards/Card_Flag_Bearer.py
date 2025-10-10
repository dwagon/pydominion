#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_FlagBearer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """When you gain or trash this, take the Flag."""
        self.name = "Flag Bearer"
        self.needsartifacts = True
        self.cost = 4

    ###########################################################################
    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.assign_artifact("Flag")
        return {}

    ###########################################################################
    def hook_trash_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.assign_artifact("Flag")
        return {}


###############################################################################
class TestFlagBearer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Flag Bearer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Flag Bearer")

    def test_gain(self) -> None:
        self.plr.gain_card("Flag Bearer")
        self.assertIsNotNone(self.plr.has_artifact("Flag"))

    def test_trash(self) -> None:
        card = self.g.get_card_from_pile("Flag Bearer")
        self.plr.add_card(card, Piles.HAND)
        self.plr.trash_card(card)
        self.assertIsNotNone(self.plr.has_artifact("Flag"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
