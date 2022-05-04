#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sentry """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Sentry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = """+1 Card; +1 Action; Look at the top 2 cards of your deck.
            Trash and/or discard any number of them. Put the rest back on top
            in any order."""
        self.name = "Sentry"
        self.cost = 5
        self.cards = 1
        self.actions = 1

    def special(self, game, player):
        cards = [player.next_card() for _ in range(2)]
        player.output(
            "Look at the top two cards of your deck. Trash, discard or move to deck"
        )
        player.output(f"Trash any/all of {self.names(cards)}")
        to_trash = player.plr_trash_card(cardsrc=cards, num=2)
        cards = [_ for _ in cards if _ not in to_trash]
        if not cards:
            return
        player.output(f"Discard any/all of {self.names(cards)}")
        to_discard = player.plr_discard_cards(cardsrc=cards, num=2)
        to_deck = [player.add_card(_, "topdeck") for _ in cards if _ not in to_discard]
        if to_deck:
            player.output(f"Moving {self.names(to_deck)} to the deck")

    def names(self, cards):
        return ", ".join([_.name for _ in cards])


###############################################################################
class Test_Sentry(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sentry"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Sentry"].remove()
        self.plr.add_card(self.card, "hand")

    def test_trash_discard(self):
        self.plr.set_deck("Copper", "Province", "Duchy")
        self.plr.test_input = ["Trash Copper", "Finish", "Discard Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIn("Province", self.plr.discardpile)

    def test_discard_keep(self):
        self.plr.set_deck("Gold", "Province", "Duchy")
        self.plr.test_input = ["Finish", "Discard Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.plr.discardpile)
        self.assertIsNotNone(self.plr.in_deck("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
