#!/usr/bin/env python

import unittest
from dominion import Card, PlayArea, Game, Piles


###############################################################################
class Card_CargoShip(Card.Card):
    """Cargo Ship"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Cargo Ship"
        self.desc = """+2 Coin; Once this turn, when you gain a card, you may
            set it aside face up (on this). At the start of your next turn,
            put it into your hand."""
        self.cost = 3
        self.coin = 2
        self._cargo_ship = PlayArea.PlayArea([])

    ###########################################################################
    def hook_gain_card(self, game, player, card):
        if self not in player.piles[Piles.DURATION]:
            return None
        if not self._cargo_ship:
            choice = player.plr_choose_options(
                f"Do you want to set {card.name} aside to play next turn?",
                ("Yes", True),
                ("No", False),
            )
            if choice:
                self._cargo_ship.add(card)
                player.secret_count += 1
                return {"dontadd": True}
        return None

    ###########################################################################
    def duration(self, game, player):
        for card in self._cargo_ship:
            player.add_card(card, Piles.HAND)
            self._cargo_ship.remove(card)
            player.secret_count -= 1


###############################################################################
class TestCargoShip(unittest.TestCase):
    """Test Cargo Ship"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cargo Ship", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card_yes(self):
        self.card = self.g.get_card_from_pile("Cargo Ship")
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.test_input = ["Yes"]
        self.plr.buy_card("Moat")
        self.assertEqual(self.card._cargo_ship[0].name, "Moat")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_card_no(self):
        self.card = self.g.get_card_from_pile("Cargo Ship")
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.test_input = ["No"]
        self.plr.buy_card("Moat")
        self.assertEqual(len(self.card._cargo_ship), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
