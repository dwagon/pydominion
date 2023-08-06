#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hovel """

import unittest
from dominion import Card, Game


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
    """botresponse"""
    return True


###############################################################################
class Test_Hovel(unittest.TestCase):
    """Test Hovel"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hovel"].remove()

    def test_trash(self):
        """Test Trashing"""
        self.plr.hand.set("Hovel")
        self.plr.test_input = ["Trash it"]
        self.plr.gain_card("Province")
        self.assertIn("Hovel", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
