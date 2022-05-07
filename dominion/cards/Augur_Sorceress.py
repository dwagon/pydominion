#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sorceress"""


import unittest
from dominion import Game, Card


###############################################################################
class Card_Sorceress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_AUGUR,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 5
        self.actions = 1
        self.name = "Sorceress"
        self.desc = """+1 Action; Name a card. Reveal the top card of your deck
            and put it into your hand. If it's the named card, each other player
            gains a Curse."""

    def special(self, game, player):
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({"selector": sel, "print": f"Guess {c.name}", "card": c})
            index += 1
        o = player.user_input(options, "Guess the top card")
        c = player.pickup_card()
        player.output(f"Next card = {c.name}, Guess = {o['card'].name}")
        if c.name == o['card'].name:
            game.output(f"Guessed {c.name} correctly")
            for plr in player.attack_victims():
                plr.gain_card("Curse")


###############################################################################
class Test_Sorceress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Augurs"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Sorceress":
                break
        self.card = card
        self.plr.add_card(self.card, "hand")

    def test_good_guess(self):
        """Play a sorceress and guess correctly"""
        self.plr.deck.set("Gold", "Gold")
        self.plr.test_input = ["Guess Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Curse", self.vic.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
