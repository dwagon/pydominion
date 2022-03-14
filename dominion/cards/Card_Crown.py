#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Crown(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_TREASURE]
        self.base = Game.EMPIRES
        self.desc = """If it's your Action phase, you may play an Action from your hand twice.
        If it's your Buy phase, you may play a Treasure from your hand twice."""
        self.name = "Crown"
        self.cost = 5

    def special(self, game, player):
        if player.phase == Card.TYPE_ACTION:
            cards = [c for c in player.hand if c.isAction()]
            self.do_twice(player, cards)
        if player.phase == "buy":
            cards = [c for c in player.hand if c.isTreasure()]
            self.do_twice(player, cards)

    def do_twice(self, player, cards):
        if not cards:
            player.output("No suitable cards")
            return
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for c in cards:
            sel = "%d" % index
            pr = "Play %s twice" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        o = player.userInput(options, "Play which card twice?")
        if not o["card"]:
            return
        for i in range(1, 3):
            player.output("Number %d play of %s" % (i, o["card"].name))
            player.play_card(o["card"], discard=False, costAction=False)
        player.discard_card(o["card"])


###############################################################################
class Test_Crown(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Crown", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Crown"].remove()

    def test_play(self):
        """Play a crown with no suitable actions"""
        self.plr.set_hand("Duchy", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.phase = Card.TYPE_ACTION
        self.plr.play_card(self.card)

    def test_action(self):
        """Play a crown with a suitable action"""
        self.plr.set_hand("Estate", "Duchy", "Copper", "Gold", "Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.phase = Card.TYPE_ACTION
        self.plr.test_input = ["moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2 * 2 - 1)

    def test_buy(self):
        """Play a crown in a buy phase"""
        self.plr.set_hand("Estate", "Duchy", "Copper", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.phase = "buy"
        self.plr.test_input = ["gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
