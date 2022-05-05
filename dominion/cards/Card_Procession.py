#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Procession(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """You may play a non-Duration Action card from your
            hand twice. Trash it. Gain an Action
            card costing exactly 1 more than it."""
        self.name = "Procession"
        self.cost = 4

    def special(self, game, player):
        actcards = [c for c in player.hand if c.isAction() and not c.isDuration()]
        if not actcards:
            player.output("No suitable action cards")
            return
        cards = player.card_sel(
            prompt="Select a card to play twice, then trash", cardsrc=actcards
        )
        if not cards:
            return
        card = cards[0]

        for i in range(1, 3):
            player.output("Play %d of %s" % (i, card.name))
            player.play_card(card, discard=False, costAction=False)
        player.trash_card(card)
        cost = player.card_cost(card) + 1
        player.plr_gain_card(cost, modifier="equal", types={Card.TYPE_ACTION: True})


###############################################################################
class Test_Procession(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Procession", "Moat", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Procession"].remove()

    def test_play(self):
        """Play procession to trash moat and buy a witch"""
        self.plr.hand.set("Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat", "Witch"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Moat"))
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertIn("Witch", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
