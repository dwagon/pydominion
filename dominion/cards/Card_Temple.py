#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Temple(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_GATHERING]
        self.base = Game.EMPIRES
        self.name = "Temple"
        self.cost = 4

    def desc(self, player):
        if player.phase == "buy":
            return """+1 VP. Trash from 1 to 3 differently named cards from your
                hand.  Add 1 VP to the Temple Supply pile. When you gain this,
                take the VP from the Temple Supply pile ({} VP).""".format(
                player.game["Temple"].getVP()
            )
        return """+1 VP. Trash from 1 to 3 differently named cards from your hand.
            Add 1 VP to the Temple Supply pile ({} VP).""".format(
            player.game["Temple"].getVP()
        )

    def special(self, game, player):
        player.addScore("Temple", 1)
        cardnames = {_.name for _ in player.hand}
        cards = [player.in_hand(_) for _ in cardnames]
        trash = player.plrTrashCard(
            cardsrc=cards, prompt="Trash up to 3 different cards", num=3
        )
        if not trash:
            return
        game["Temple"].addVP()

    def hook_gain_this_card(self, game, player):
        score = game["Temple"].drainVP()
        player.output("Gaining %d VP from Temple" % score)
        player.addScore("Temple", score)


###############################################################################
class Test_Temple(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Temple"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Temple"].remove()

    def test_play(self):
        """Play a Temple"""
        self.plr.setHand("Copper", "Silver", "Silver", "Gold", "Duchy")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Copper", "Silver", "finish"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()["Temple"], 1)
        self.assertIsNotNone(self.g.in_trash("Silver"))

    def test_gain(self):
        """Gain a Temple"""
        self.g["Temple"].addVP(5)
        self.plr.setCoin(4)
        self.plr.buyCard(self.g["Temple"])
        self.assertEqual(self.plr.getScoreDetails()["Temple"], 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
