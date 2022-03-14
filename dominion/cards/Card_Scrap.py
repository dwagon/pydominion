#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Scrap """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Scrap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """Trash a card from your hand.
            Choose a different thing per coin it costs: +1 Card; +1 Action; +1 Buy;
            +1 Coin; gain a Silver; gain a Horse."""
        self.name = "Scrap"
        self.cost = 3
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        trc = player.plrTrashCard(
            printcost=True, prompt="Trash a card from your hand for benefits"
        )
        if not trc:
            return
        cost = player.cardCost(trc[0])
        if cost >= 1:
            player.pickup_card()
        if cost >= 2:
            player.addActions(1)
        if cost >= 3:
            player.addBuys(1)
        if cost >= 4:
            player.addCoin(1)
        if cost >= 5:
            player.gainCard("Silver")
            player.output("Gained a Silver")
        if cost >= 6:
            player.gainCard("Horse")
            player.output("Gained a Horse")


###############################################################################
class Test_Scrap(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Scrap"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Scrap"].remove()

    def test_playcard_cost0(self):
        """Play a scrap and trash something worth 0"""
        self.plr.set_hand("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Copper"))

    def test_playcard_cost3(self):
        """Play a scrap and trash something worth 3"""
        self.plr.set_hand("Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.set_deck("Province")
        self.plr.test_input = ["trash silver"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Silver"))
        self.assertIsNotNone(self.plr.in_hand("Province"))
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_playcard_cost6(self):
        """Play a scrap and trash something worth more than 6"""
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.set_deck("Copper")
        self.plr.test_input = ["trash province"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertIsNotNone(self.plr.in_hand("Copper"))
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Horse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
