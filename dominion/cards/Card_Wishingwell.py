#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_WishingWell(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+1 Card +1 Action;
        Name a card, then reveal the top card of your deck. If it's the named card, put it into your hand."""
        self.name = "Wishing Well"
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game, player):
        """Name a card. Reveal the top card of your deck. If it's
        the named card, put it into your hand"""
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for name, card_pile in sorted(game.get_card_piles()):
            options.append(
                {"selector": f"{index}", "print": f"Guess {name}", "card": name}
            )
            index += 1
        o = player.user_input(options, "Guess the top card")
        if not o["card"]:
            return
        card = player.next_card()
        if not card:
            return
        player.reveal_card(card)
        if o["card"] == card.name:
            player.output("You guessed correctly")
            player.add_card(card, Piles.HAND)
        else:
            player.output(f"You chose poorly - it was a {card}")
            player.add_card(card, "topdeck")


###############################################################################
class TestWishingWell(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Wishing Well"],
            badcards=["Fool's Gold", "Tournament", "Pooka"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Wishing Well")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """No guess still gets a card and action"""
        self.plr.test_input = ["no guess"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_good(self):
        """A good guess means the card ends up in the hand"""
        self.plr.piles[Piles.DECK].set("Silver", "Copper")
        self.plr.test_input = ["Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])

    def test_bad(self):
        """Guessing badly should result in the card staying on the deck"""
        self.plr.piles[Piles.DECK].set("Province", "Copper")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
