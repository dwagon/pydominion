#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Mastermind """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Mastermind(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """At the start of your next turn, you may play an Action card from your hand three times."""
        self.name = "Mastermind"
        self.cost = 5

    def duration(self, game, player):
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for c in player.piles[Piles.HAND]:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s thrice" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        if index == 1:
            player.output("No action cards to repeat")
            return
        o = player.user_input(options, "Play which action card three times?")
        if not o["card"]:
            return
        for i in range(1, 4):
            player.output(f"Number {i} play of {o['card'].name}")
            player.play_card(o["card"], discard=False, cost_action=False)
        player.add_card(o["card"], "played")
        player.piles[Piles.HAND].remove(o["card"])


###############################################################################
class Test_Mastermind(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mastermind", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mastermind"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a card"""
        self.plr.piles[Piles.DISCARD].set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Play Moat"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
