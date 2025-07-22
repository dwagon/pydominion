#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Bounty_Hunter"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Bounty_Hunter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Action; Exile a card from your hand. If you didn't
            have a copy of it in Exile, +3 Coin."""
        self.name = "Bounty Hunter"
        self.cost = 4
        self.actions = 1

    def special(self, game, player):
        if crd := player.card_sel(prompt="Exile a card", verbs=("Exile", "Unexile")):
            if crd[0] not in player.piles[Piles.EXILE]:
                player.coins.add(3)
            player.move_card(crd[0], Piles.EXILE)


###############################################################################
class TestBountyHunter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bounty Hunter"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Bounty Hunter")

    def test_play(self):
        self.plr.piles[Piles.EXILE].set("Copper")
        self.plr.piles[Piles.HAND].set("Silver", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Exile Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
