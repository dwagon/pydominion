#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Kiln """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Kiln(Card.Card):
    """Kiln"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+$2; The next time you play a card this turn, you may first gain a copy of it."""
        self.name = "Kiln"
        self.coin = 2
        self.cost = 5

    def hook_pre_action(self, game, player, card):  # pylint: disable=unused-argument
        """The next time you play a card this turn, you may first gain a copy of it."""
        opt = player.plr_choose_options(
            f"Gain a copy of {card.name}?",
            ("Do nothing", False),
            (f"Gain {card.name}", True),
        )
        if opt:
            player.gain_card(card.name)


###############################################################################
class Test_Kiln(unittest.TestCase):
    """Test Kiln"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Kiln", "Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Kiln"].remove()
        self.village = self.g["Village"].remove()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.add_card(self.village, Piles.HAND)

    def test_play(self):
        """Test play and gain card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.actions.set(1)
        self.plr.test_input = ["Gain"]
        self.plr.play_card(self.village)
        self.assertIn("Village", self.plr.piles[Piles.DISCARD])
        self.assertIn("Village", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
