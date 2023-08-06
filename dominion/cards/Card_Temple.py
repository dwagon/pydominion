#!/usr/bin/env python

import unittest
from dominion import Card, Game, Player


###############################################################################
class Card_Temple(Card.Card):
    """Temple"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.GATHERING]
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Temple"
        self.cost = 4

    def desc(self, player):
        """Variable Description"""
        if player.phase == Player.Phase.BUY:
            return f"""+1 VP. Trash from 1 to 3 differently named cards from your
                hand.  Add 1 VP to the Temple Supply pile. When you gain this,
                take the VP from the Temple Supply pile ({player.game["Temple"].getVP()} VP)."""
        return f"""+1 VP. Trash from 1 to 3 differently named cards from your hand.
            Add 1 VP to the Temple Supply pile ({player.game["Temple"].getVP()} VP)."""

    def special(self, game, player):
        player.add_score("Temple", 1)
        cardnames = {_.name for _ in player.hand}
        cards = [player.hand[_] for _ in cardnames]
        trash = player.plr_trash_card(cardsrc=cards, prompt="Trash up to 3 different cards", num=3)
        if not trash:
            return
        game["Temple"].addVP()

    def hook_gain_this_card(self, game, player):
        score = game["Temple"].drainVP()
        player.output(f"Gaining {score} VP from Temple")
        player.add_score("Temple", score)


###############################################################################
class Test_Temple(unittest.TestCase):
    """Test Temple"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Temple"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Temple"].remove()

    def test_play(self):
        """Play a Temple"""
        self.plr.hand.set("Copper", "Silver", "Silver", "Gold", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Copper", "Silver", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Temple"], 1)
        self.assertIn("Silver", self.g.trashpile)

    def test_gain(self):
        """Gain a Temple"""
        self.g["Temple"].addVP(5)
        self.plr.coins.set(4)
        self.plr.buy_card(self.g["Temple"])
        self.assertEqual(self.plr.get_score_details()["Temple"], 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
