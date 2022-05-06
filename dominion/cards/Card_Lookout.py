#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Lookout(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """+1 Action; Look at the top 3 cards of your deck.
            Trash one of them. Discard one of them. Put the other one on top of
            your deck"""
        self.name = "Lookout"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """Look at the top 3 cards of your deck. Trash one of them.
        Discard one of them. Put the other one on top of your deck
        """
        cards = []
        for _ in range(3):
            cards.append(player.next_card())
        cards = [c for c in cards if c]
        if not cards:
            player.output("No cards available")
            return
        player.output("Pulled %s from deck" % ", ".join([c.name for c in cards]))
        player.output("Trash a card, Discard a card, put a card on your deck")
        tc = self.trash(player, cards)
        cards.remove(tc)
        cd = self.discard(player, cards)
        cards.remove(cd)
        player.output("Putting %s on top of deck" % cards[0].name)
        player.add_card(cards[0], "topdeck")

    def trash(self, player, cards):
        index = 1
        options = []
        for c in cards:
            sel = "%d" % index
            index += 1
            options.append({"selector": sel, "print": "Trash %s" % c.name, "card": c})
        o = player.user_input(options, "Select a card to trash")
        player.trash_card(o["card"])
        return o["card"]

    def discard(self, player, cards):
        index = 1
        options = []
        for c in cards:
            sel = "%d" % index
            index += 1
            options.append({"selector": sel, "print": "Discard %s" % c.name, "card": c})
        o = player.user_input(options, "Select a card to discard")
        player.discard_card(o["card"])
        return o["card"]


###############################################################################
class Test_Lookout(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Lookout"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.lookout = self.g["Lookout"].remove()

    def test_actions(self):
        self.plr.deck.set("Copper", "Estate", "Gold", "Province")
        self.plr.add_card(self.lookout, "hand")
        self.plr.test_input = ["Province", "Gold"]
        self.plr.play_card(self.lookout)
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertIn("Gold", self.plr.discardpile)
        self.assertEqual(self.plr.deck[0].name, "Copper")
        self.assertEqual(self.plr.deck[1].name, "Estate")

    def test_nocards(self):
        """Play a lookout when there are no cards available"""
        tsize = self.g.trash_size()
        self.plr.deck.set()
        self.plr.add_card(self.lookout, "hand")
        self.plr.play_card(self.lookout)
        self.assertEqual(self.g.trash_size(), tsize)
        self.assertEqual(self.plr.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
