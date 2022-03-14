#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Broker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Broker"
        self.desc = """Trash a card from your hand and choose one:
            +1 Card per $1 it costs; or +1 Action per $1 it costs;
            or +$1 per $1 it costs; or +1 Favor per $1 it costs."""
        self.cost = 4

    def special(self, game, player):
        tr = player.plrTrashCard(printcost=True)
        cost = tr[0].cost
        if cost == 0:
            return
        options = []
        options.append((f"+{cost} cards", "card"))
        options.append((f"+{cost} actions", "action"))
        options.append((f"+${cost} coins", "cash"))
        options.append((f"+{cost} favors", "favor"))
        dc = player.plrChooseOptions("Pick one:", *options)
        if dc == "card":
            player.pickup_cards(cost)
        elif dc == "action":
            player.addActions(cost)
        elif dc == "cash":
            player.addCoin(cost)
        elif dc == "favor":
            player.addFavor(cost)


###############################################################################
class Test_Broker(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Broker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Broker"].remove()

    def test_play_cards(self):
        """Play the card - gain cards"""
        self.plr.set_hand("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "cards"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2 + 2)

    def test_play_action(self):
        """Play the card - gain action"""
        self.plr.set_hand("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "actions"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_play_cash(self):
        """Play the card - gain cash"""
        self.plr.set_hand("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "coins"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_play_favor(self):
        """Play the card - gain favor"""
        fav = self.plr.getFavor()
        self.plr.set_hand("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "favor"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getFavor(), fav + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
