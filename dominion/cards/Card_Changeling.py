#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Changeling(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
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
            f"Swap {card.name} for a Changeling?",
            (f"Swap {card.name}", True),
            (f"Keep {card.name}", False),
        )
        if swap:
            return {"replace": "Changeling"}
        return None

    def night(self, game, player):
        options = [{"selector": "0", "print": "Keep Changeling", "card": None}]
        index = 1
        for card in player.played + player.hand:
            sel = f"{index}"
            pr = f"Exchange for {card.name}"
            options.append({"selector": sel, "print": pr, "card": card})
            index += 1
        o = player.user_input(options, "Trash Changeling to gain a card")
        if o["card"]:
            player.trash_card(self)
            player.gain_card(o["card"].name)


###############################################################################
class Test_Changeling(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Changeling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Changeling"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_keep(self):
        self.plr.phase = "night"
        self.plr.test_input = ["Keep Changeling"]
        self.plr.play_card(self.card)
        self.assertIn("Changeling", self.plr.played)

    def test_play_swap(self):
        self.plr.phase = "night"
        self.plr.played.set("Gold")
        self.plr.test_input = ["Exchange for Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertIn("Changeling", self.g.trashpile)

    def test_gain_keep(self):
        self.plr.test_input = ["Keep Silver"]
        self.plr.gain_card("Silver")
        self.assertIn("Silver", self.plr.discardpile)

    def test_gain_swap(self):
        self.plr.test_input = ["Swap Silver"]
        self.plr.gain_card("Silver")
        self.assertNotIn("Silver", self.plr.discardpile)
        self.assertIn("Changeling", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
