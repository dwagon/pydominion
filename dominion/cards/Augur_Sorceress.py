#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sorceress"""


import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Sorceress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.AUGUR]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.actions = 1
        self.required_cards = ["Curse"]
        self.name = "Sorceress"
        self.desc = """+1 Action; Name a card. Reveal the top card of your deck
            and put it into your hand. If it's the named card, each other player
            gains a Curse."""

    def special(self, game, player):
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for name, card_pile in sorted(game.card_piles()):
            sel = f"{index}"
            options.append(
                {"selector": sel, "print": f"Guess {name}", "card": card_pile}
            )
            index += 1
        o = player.user_input(options, "Guess the top card")
        if not o["card"]:
            player.output("No suitable cards")
            return
        card_pile = player.pickup_card()
        player.output(f"Next card = {card_pile}, Guess = {o['card']}")
        if card_pile.name == o["card"].name:
            game.output(f"Guessed {card_pile} correctly")
            for plr in player.attack_victims():
                plr.gain_card("Curse")


###############################################################################
class TestSorceress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Augurs"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Sorceress":
                break
        self.card = card
        self.plr.add_card(self.card, Piles.HAND)

    def test_good_guess(self):
        """Play a sorceress and guess correctly"""
        self.plr.piles[Piles.DECK].set("Gold", "Gold")
        self.plr.test_input = ["Guess Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
