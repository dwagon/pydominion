#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Lich(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.WIZARD,  # pylint: disable=no-member
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.cards = 6
        self.actions = 2
        self.name = "Lich"
        self.pile = "Wizards"
        self.desc = """+6 Cards; +2 Actions; Skip a turn;
            When you trash this, discard it and gain a cheaper card from the trash."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.skip_turn = True

    def hook_trash_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """Discard rather than trash"""
        player.add_card(self, "discard")
        player.piles[Piles.HAND].remove(self)
        in_trash = [_ for _ in game.trash_pile if _.cost < self.cost]
        if in_trash:
            crd = player.plr_pick_card(cardsrc=in_trash, force=True, num=1)
            if not crd:
                return {}
            player.gain_card(new_card=crd)
            game.trash_pile.remove(crd)
        return {OptionKeys.TRASH: False}


###############################################################################
class Test_Lich(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g.get_card_from_pile("Wizards")
            if card.name == "Lich":
                break
        self.card = card

    def test_play(self) -> None:
        """Play a lich"""
        hndsz = self.plr.piles[Piles.HAND].size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DISCARD].set("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz + 6)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_trash(self) -> None:
        """Trash the lich"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Silver"]
        self.g.trash_pile.set("Silver")
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertNotIn("Lich", self.g.trash_pile)
        self.assertNotIn("Silver", self.g.trash_pile)
        self.assertIn("Lich", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
