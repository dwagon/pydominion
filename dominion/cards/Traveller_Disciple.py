#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Disciple(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """You may play an Action card from your hand twice. Gain a copy of it"""
        self.name = "Disciple"
        self.purchasable = False
        self.numcards = 5
        self.cost = 5

    def special(self, game, player):
        """You may play an Action card from your hand twice. Gain a copy of it"""
        actions = [c for c in player.hand if c.isAction()]
        if not actions:
            player.output("No suitable actions to perform")
            return
        cards = player.card_sel(cardsrc=actions)
        if not cards:
            return
        card = cards[0]
        for i in range(1, 3):
            player.output("Number %d play of %s" % (i, card.name))
            player.play_card(card, discard=False, costAction=False)
        player.add_card(card, "played")
        player.hand.remove(card)
        if card.purchasable:
            c = player.gain_card(card.name)
            if c:
                player.output("Gained a %s from Disciple" % c.name)

    def hook_discard_this_card(self, game, player, source):
        """Replace with Teacher"""
        player.replace_traveller(self, "Teacher")


###############################################################################
class Test_Disciple(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Peasant", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Disciple"].remove()

    def test_play_no_actions(self):
        """Play a disciple with no actions available"""
        self.plr.hand.set("Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.played.size(), 1)

    def test_play_actions(self):
        """Play a disciple with an action available"""
        self.plr.hand.set("Copper", "Estate", "Moat")
        self.plr.test_input = ["moat"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.played.size(), 2)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertIn("Moat", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
