#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Jack_of_all_Trades(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """Gain a Silver.
            Look at the top card of your deck; discard it or put it back.
            Draw until you have 5 cards in your hand.
            You may trash a card from your hand that is not a Treasure."""
        self.name = "Jack of all Trades"
        self.cost = 4

    def special(self, game, player):
        player.gain_card("Silver")

        card = player.next_card()
        topdeck = player.plr_choose_options(
            "Put %s back on top of your deck?" % card.name,
            ("Discard %s" % card.name, False),
            ("Keep %s on top of your deck" % card.name, True),
        )
        if topdeck:
            player.add_card(card, "topdeck")
        else:
            player.discard_card(card)

        while player.hand.size() < 5:
            player.pickup_card()

        cards = [c for c in player.hand if not c.isTreasure()]
        if cards:
            player.plr_trash_card(cardsrc=cards, prompt="Trash a non-Treasure")


###############################################################################
class Test_Jack_of_all_Trades(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Jack of all Trades"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Jack of all Trades"].remove()

    def test_play(self):
        """Play a Jack of all Trades"""
        tsize = self.g.trashSize()
        self.plr.set_deck("Copper", "Copper", "Copper", "Copper", "Copper", "Gold")
        self.plr.set_hand("Duchy")
        self.plr.test_input = ["keep", "duchy"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)

        self.assertIsNotNone(self.plr.in_discard("Silver"))  # Gain a Silver

        self.assertIsNotNone(self.plr.in_hand("Gold"))  # Keep on deck, then picked up

        self.assertEqual(self.plr.hand.size(), 5 - 1)  # One trashed
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Duchy"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
