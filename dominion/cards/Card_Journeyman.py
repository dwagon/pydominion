#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Journeyman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.GUILDS
        self.desc = """Name a card.
        Reveal cards from the top of your deck until you reveal 3 cards that are not the named card.
        Put those cards into your hand and discard the rest."""
        self.name = "Journeyman"
        self.cost = 5

    def special(self, game, player):
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({"selector": sel, "print": "Guess %s" % c.name, "card": c})
            index += 1
        o = player.user_input(
            options,
            "Name a card. Reveal cards from your deck until you have 3 that aren't the named card",
        )
        cards = []
        while len(cards) < 3:
            card = player.next_card()
            player.reveal_card(card)
            if card.name == o["card"].name:
                player.output("Discarding %s" % card.name)
                player.discard_card(card)
            else:
                cards.append(card)
        for card in cards:
            player.add_card(card, "hand")
            player.output("Pulling %s into hand" % card.name)


###############################################################################
class Test_Journeyman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Journeyman"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Journeyman"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_card(self):
        """Play the pawn - select card and action"""
        self.plr.set_deck("Copper", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.discardpile)
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertIsNotNone(self.plr.in_hand("Province"))
        self.assertIsNotNone(self.plr.in_hand("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
