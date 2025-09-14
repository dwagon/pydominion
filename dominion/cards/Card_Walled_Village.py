#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Walled_Village"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, PlayArea, OptionKeys

WALLED_VILLAGE = "walled village"


###############################################################################
class Card_Walled_Village(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROMO
        self.desc = """+1 Card, +2 Actions; At the start of Clean-up,
        if you have this and no more than one other Action card in play, you may put this onto your deck"""
        self.name = "Walled Village"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """At the start of Clean-up, if you have this and no more than one other Action card in play,
        you may put this onto your deck"""
        if WALLED_VILLAGE not in player.specials:
            player.specials[WALLED_VILLAGE] = PlayArea.PlayArea(initial=None)
        num_actions = sum(1 for card in player.piles[Piles.PLAYED] if card.isAction())
        if num_actions > 2:
            return {}
        if self not in player.piles[Piles.PLAYED]:
            return {}
        player.move_card(self, player.specials[WALLED_VILLAGE])
        player.secret_count += 1
        return {}

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if WALLED_VILLAGE not in player.specials:
            return
        for card in player.specials[WALLED_VILLAGE]:
            player.secret_count -= 1
            player.output(f"Returning {card} to deck")
            player.move_card(card, Piles.HAND)
        player.specials[WALLED_VILLAGE] = PlayArea.PlayArea(initial=None)


###############################################################################
class Test_Walled_Village(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Walled Village", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Walled Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a Walled Village"""
        actions = self.plr.actions.get()
        hand_size = self.plr.piles[Piles.HAND].size()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hand_size + 1 - 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Walled Village", self.plr.piles[Piles.HAND])

    def test_play_no_return(self) -> None:
        """Play a Walled Village so that we don't get it back"""
        # Fill discard so we don't need to shuffle the Walled Village back in to refill hand
        self.plr.piles[Piles.DECK].set(
            "Copper", "Silver", "Gold", "Estate", "Duchy", "Province", "Copper", "Silver", "Gold", "Estate"
        )
        moat1 = self.g.get_card_from_pile("Moat")
        moat2 = self.g.get_card_from_pile("Moat")
        self.plr.play_card(self.card)
        self.plr.play_card(moat1)
        self.plr.play_card(moat2)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Walled Village", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
