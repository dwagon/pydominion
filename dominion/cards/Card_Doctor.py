#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Doctor(Card.Card):
    """Doctor"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.name = "Doctor"
        self.overpay = True
        self.cost = 3

    def desc(self, player):
        """Variable description"""
        if player.phase == Player.Phase.BUY:
            return """Name a card. Reveal the top 3 cards of your deck.
                Trash the matches. Put the rest back on top in any order.
                When you buy this, you may overpay for it. For each 1 you overpaid,
                look at the top card of your deck; trash it, discard it,
                or put it back."""
        return """Name a card. Reveal the top 3 cards of your deck.
            Trash the matches. Put the rest back on top in any order."""

    def special(self, game, player):
        options = []
        index = 1
        for c in sorted(game.cardTypes()):
            sel = f"{index}"
            options.append({"selector": sel, "print": f"Guess {c.name}", "card": c})
            index += 1
        o = player.user_input(
            options, "Pick which card to trash if it is in the top 3 of your deck"
        )
        cards = []
        for _ in range(3):
            cards.append(player.next_card())
        for card in cards:
            player.reveal_card(card)
            if card.name == o["card"].name:
                player.output(f"Trashing {card.name}")
                card.location = None
                player.trash_card(card)
            else:
                player.output(f"Putting {card.name} back")
                player.add_card(card, "topdeck")

    def hook_overpay(self, game, player, amount):
        """For each 1 you overpaid, look at the top card of your deck; trash it,
        discard it, or put it back."""
        for i in range(amount):
            player.output(f"Doctoring {i+1}/{amount}")
            card = player.next_card()
            options = []
            options.append(
                {
                    "selector": "0",
                    "print": "Put {card.name} back on top",
                    "action": "put back",
                }
            )
            options.append(
                {
                    "selector": "1",
                    "print": "Trash {card.name}",
                    "action": "trash",
                }
            )
            options.append(
                {
                    "selector": "2",
                    "print": f"Discard {card.name}",
                    "action": "discard",
                }
            )
            o = player.user_input(options, f"What to do with the top card {card.name}?")
            if o["action"] == "trash":
                card.location = None
                player.trash_card(card)
                player.output(f"Trashing {card.name}")
            elif o["action"] == "discard":
                player.add_card(card, "discard")
                player.output(f"Discarding {card.name}")
            elif o["action"] == "put back":
                player.add_card(card, "topdeck")
                player.output(f"Putting {card.name} back")


###############################################################################
class Test_Doctor(unittest.TestCase):
    """Test Doctor"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Doctor"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Doctor"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play the Doctor"""
        self.plr.piles[Piles.DECK].set("Silver", "Province", "Duchy")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trashpile)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])

    def test_buy(self):
        """Buy a Doctor"""
        self.plr.coins.set(6)
        self.plr.test_input = ["3", "trash", "discard", "back on top"]
        self.plr.piles[Piles.DECK].set("Silver", "Province", "Duchy")
        self.plr.buy_card(self.g["Doctor"])
        self.assertIn("Duchy", self.g.trashpile)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
