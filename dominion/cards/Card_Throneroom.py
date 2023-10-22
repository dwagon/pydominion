#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_ThroneRoom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Play action twice"
        self.name = "Throne Room"
        self.cost = 4

    def special(self, game, player):
        """You may choose an Action card in your hand. Play it twice"""
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for card in player.piles[Piles.HAND]:
            if not card.isAction():
                continue
            options.append(
                {"selector": f"{index}", "print": f"Play {card} twice", "card": card}
            )
            index += 1
        if index == 1:
            return
        o = player.user_input(options, "Play which action card twice?")
        if not o["card"]:
            return
        for i in range(1, 3):
            player.output(f"Number {i} play of {o['card']}'")
            player.play_card(o["card"], discard=False, cost_action=False)
        player.discard_card(o["card"])


###############################################################################
class TestThroneRoom(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Throne Room", "Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_action(self):
        # Test by playing mine twice on a copper. Cu -> Ag -> Au
        self.plr.piles[Piles.HAND].set("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        self.plr.test_input = ["1", "1", "1"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Gold")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Mine")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_do_nothing(self):
        self.plr.piles[Piles.HAND].set("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(card)

    def test_no_action(self):
        self.plr.piles[Piles.HAND].set("Copper", "Copper")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.test_input, ["0"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
