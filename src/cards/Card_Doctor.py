#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Doctor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.GUILDS
        self.name = "Doctor"
        self.overpay = True
        self.cost = 3

    def desc(self, player):
        if player.phase == "buy":
            return """Name a card. Reveal the top 3 cards of your deck.
                Trash the matches. Put the rest back on top in any order.
                When you buy this, you may overpay for it. For each 1 you overpaid,
                look at the top card of your deck; trash it, discard it,
                or put it back."""
        return "Name a card. Reveal the top 3 cards of your deck. Trash the matches. Put the rest back on top in any order."

    def special(self, game, player):
        options = []
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({"selector": sel, "print": "Guess %s" % c.name, "card": c})
            index += 1
        o = player.userInput(
            options, "Pick which card to trash if it is in the top 3 of your deck"
        )
        cards = []
        for _ in range(3):
            cards.append(player.nextCard())
        for card in cards:
            player.revealCard(card)
            if card.name == o["card"].name:
                player.output("Trashing %s" % card.name)
                player.trashCard(card)
            else:
                player.output("Putting %s back" % card.name)
                player.addCard(card, "topdeck")

    def hook_overpay(self, game, player, amount):
        for i in range(amount):
            player.output("Doctoring %d/%d" % (i + 1, amount))
            card = player.nextCard()
            options = []
            options.append(
                {
                    "selector": "0",
                    "print": "Put %s back on top" % card.name,
                    Card.TYPE_ACTION: "put back",
                }
            )
            options.append(
                {
                    "selector": "1",
                    "print": "Trash %s" % card.name,
                    Card.TYPE_ACTION: "trash",
                }
            )
            options.append(
                {
                    "selector": "2",
                    "print": "Discard %s" % card.name,
                    Card.TYPE_ACTION: "discard",
                }
            )
            o = player.userInput(
                options, "What to do with the top card %s?" % card.name
            )
            if o[Card.TYPE_ACTION] == "trash":
                player.trashCard(card)
                player.output("Trashing %s" % card.name)
            elif o[Card.TYPE_ACTION] == "discard":
                player.addCard(card, "discard")
                player.output("Discarding %s" % card.name)
            elif o[Card.TYPE_ACTION] == "put back":
                player.addCard(card, "topdeck")
                player.output("Putting %s back" % card.name)


###############################################################################
class Test_Doctor(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Doctor"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Doctor"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play_card(self):
        """Play the Doctor"""
        self.plr.setDeck("Silver", "Province", "Duchy")
        self.plr.test_input = ["Province"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertIsNotNone(self.plr.in_deck("Silver"))
        self.assertIsNotNone(self.plr.in_deck("Duchy"))

    def test_buy(self):
        """Buy a Doctor"""
        self.plr.coin = 6
        self.plr.test_input = ["3", "trash", "discard", "back on top"]
        self.plr.setDeck("Silver", "Province", "Duchy")
        self.plr.buyCard(self.g["Doctor"])
        self.assertIsNotNone(self.g.in_trash("Duchy"))
        self.assertIsNotNone(self.plr.in_discard("Province"))
        self.assertEqual(self.plr.deck[-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
