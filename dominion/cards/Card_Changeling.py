#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Changeling(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT]
        self.base = Game.NOCTURNE
        self.desc = """Trash this. Gain a copy of a card you have in play.
In games using this, when you gain a card costing 3 or more, you may exchange it for a Changeling."""
        self.name = "Changeling"
        self.cost = 3

    def hook_gain_card(self, game, player, card):
        if card.cost < 3:
            return None
        if game["Changeling"].is_empty():
            return None
        swap = player.plr_choose_options(
            "Swap {} for a Changeling?".format(card.name),
            ("Swap {}".format(card.name), True),
            ("Keep {}".format(card.name), False),
        )
        if swap:
            return {"replace": "Changeling"}
        return None

    def night(self, game, player):
        options = [{"selector": "0", "print": "Keep Changeling", "card": None}]
        index = 1
        for card in player.played + player.hand:
            sel = "{}".format(index)
            pr = "Exchange for {}".format(card.name)
            options.append({"selector": sel, "print": pr, "card": card})
            index += 1
        o = player.userInput(options, "Trash Changeling to gain a card")
        if o["card"]:
            player.trash_card(self)
            player.gain_card(o["card"].name)


###############################################################################
class Test_Changeling(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Changeling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Changeling"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_keep(self):
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.test_input = ["Keep Changeling"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_played("Changeling"))

    def test_play_swap(self):
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.set_played("Gold")
        self.plr.test_input = ["Exchange for Gold"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertIsNotNone(self.g.in_trash("Changeling"))

    def test_gain_keep(self):
        self.plr.test_input = ["Keep Silver"]
        self.plr.gain_card("Silver")
        self.assertIsNotNone(self.plr.in_discard("Silver"))

    def test_gain_swap(self):
        self.plr.test_input = ["Swap Silver"]
        self.plr.gain_card("Silver")
        self.assertIsNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Changeling"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
