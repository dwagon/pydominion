#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hovel """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Hovel(Card.Card):
    """Hovel"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.REACTION, Card.CardType.SHELTER]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "When you gain a Victory card, you may trash this from your hand."
        self.name = "Hovel"
        self.cost = 1
        self.purchasable = False
        self.victory = 0
        self.pile = "Shelters"

    def hook_gain_card(self, game, player, card):
        if not card.isVictory():
            return
        to_trash = player.plr_choose_options(
            "Trash Hovel?", ("Trash it", True), ("Keep it", False)
        )
        if to_trash:
            player.trash_card(self)


###############################################################################
def botresponse(
    player, kind, args=None, kwargs=None
):  # pragma: no cover, pylint: disable=unused-argument
    """bot response"""
    return True


###############################################################################
class TestHovel(unittest.TestCase):
    """Test Hovel"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_trash(self):
        """Test Trashing"""
        hovel = self.g.get_card_from_pile("Shelters", "Hovel")
        self.plr.piles[Piles.HAND].empty()
        self.plr.piles[Piles.HAND].add(hovel)
        self.g.print_state()
        self.plr.test_input = ["Trash it"]
        self.plr.gain_card("Province")
        self.assertIn("Hovel", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
