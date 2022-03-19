#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game


###############################################################################
class Card_Archive(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.EMPIRES
        self.desc = """+1 Action; Set aside the top 3 cards of your deck face
            down (you may look at them). Now and at the start of your next two turns,
            put one into your hand."""
        self.name = "Archive"
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        if not hasattr(player, "_archive_reserve"):
            player._archive_reserve = PlayArea.PlayArea([])
        for _ in range(3):
            card = player.next_card()
            player.output("Putting {} in the archive".format(card.name))
            player._archive_reserve.add(card)
            player.secret_count += 1
        self.permanent = True

    def duration(self, game, player):
        options = []
        index = 0
        for card in player._archive_reserve:
            sel = "{}".format(index)
            toprint = "Bring back {}".format(card.name)
            options.append({"selector": sel, "print": toprint, "card": card})
            index += 1
        o = player.user_input(options, "What card to bring back from the Archive?")
        player.add_card(o["card"], "hand")
        player._archive_reserve.remove(o["card"])
        player.secret_count -= 1
        if player._archive_reserve.is_empty():
            self.permanent = False


###############################################################################
class Test_Archive(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Archive"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Archive"].remove()

    def test_play(self):
        """Play a Archive"""
        self.plr.set_deck("Gold", "Silver", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Gold"]
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertEqual(len(self.plr._archive_reserve), 2)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Silver"]
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.in_hand("Silver"))
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Province"]
        self.plr.start_turn()
        self.assertFalse(self.card.permanent)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
