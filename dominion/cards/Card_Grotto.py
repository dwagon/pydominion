#!/usr/bin/env python
# pylint: disable=protected-access

import unittest

from dominion import Card, Game, PlayArea, Piles, Player, OptionKeys

GROTTO = "grotto"


###############################################################################
class Card_Grotto(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.desc = """+1 Action; Set aside up to 4 cards from your hand face down (on this).
        At the start of your next turn, discard them, then draw as many."""
        self.name = "Grotto"
        self.base = Card.CardExpansion.PLUNDER
        self.actions = 1
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if GROTTO not in player.specials:
            player.specials[GROTTO] = PlayArea.PlayArea(initial=[])
        player.output("Set aside up to 4 cards on Grotto")
        for _ in range(4):
            if not self._set_aside(player):
                break

    def _set_aside(self, player: Player.Player) -> bool:
        """Select a card to put on to Grotto; return True if card selected"""
        card = player.plr_pick_card()
        if not card:
            return False
        player.output(f"Adding {card} to the Grotto")
        player.piles[Piles.HAND].remove(card)
        player.specials[GROTTO].add(card)
        player.secret_count += 1
        return True

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        for card in player.specials[GROTTO]:
            player.specials[GROTTO].remove(card)
            player.discard_card(card)
            player.secret_count -= 1
            player.pickup_card()
        return {}


###############################################################################
class TestGrotto(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Grotto"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Grotto")

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Copper", "Select Duchy", "Select Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(len(self.plr.specials[GROTTO]), 3)
        self.assertEqual(self.plr.secret_count, 3)
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])

        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
