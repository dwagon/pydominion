#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Broker """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Broker(Card.Card):
    """Broker"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Broker"
        self.desc = """Trash a card from your hand and choose one:
            +1 Card per $1 it costs; or +1 Action per $1 it costs;
            or +$1 per $1 it costs; or +1 Favor per $1 it costs."""
        self.cost = 4

    def special(self, game, player):
        tr = player.plr_trash_card(printcost=True)
        if not tr:
            return
        cost = tr[0].cost
        if cost == 0:
            return
        options = []
        options.append((f"+{cost} cards", "card"))
        options.append((f"+{cost} actions", "action"))
        options.append((f"+${cost} coins", "cash"))
        options.append((f"+{cost} favors", "favor"))
        dc = player.plr_choose_options("Pick one:", *options)
        if dc == "card":
            player.pickup_cards(cost)
        elif dc == "action":
            player.add_actions(cost)
        elif dc == "cash":
            player.coins.add(cost)
        elif dc == "favor":
            player.favors.add(cost)


###############################################################################
class Test_Broker(unittest.TestCase):
    """Test Broker"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Broker"],
            ally="Plateau Shepherds",
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Broker"].remove()

    def test_play_cards(self):
        """Play the card - gain cards"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Estate", "cards"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 2)

    def test_play_nothing(self):
        """Play but select nothing to trash"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["finish"]
        tsize = self.g.trash_pile.size()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_play_action(self):
        """Play the card - gain action"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Estate", "actions"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_play_cash(self):
        """Play the card - gain cash"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Estate", "coins"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_play_favor(self):
        """Play the card - gain favor"""
        self.plr.favors.set(0)
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy", "Copper", "Province", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Estate", "favor"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
