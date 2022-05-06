#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Mystic(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = "+2 coin, +1 action; Name a card. Reveal the top card of your deck. If it's the named card, put it into your hand."
        self.name = "Mystic"
        self.actions = 1
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """ " Name a card. Reveal the top card of your deck. If it's
        the named card, put it into your hand"""
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({"selector": sel, "print": "Guess %s" % c.name, "card": c})
            index += 1
        o = player.user_input(options, "Guess the top card")
        if not o["card"]:
            return
        c = player.next_card()
        player.reveal_card(c)
        if o["card"].name == c.name:
            player.output("You guessed correctly")
            player.add_card(c, "hand")
        else:
            player.output("You chose poorly - it was a %s" % c.name)
            player.add_card(c, "topdeck")


###############################################################################
class Test_Mystic(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Mystic"],
            badcards=["Tournament", "Fool's Gold", "Pooka"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mystic"].remove()

    def test_play(self):
        """No guess should still get results"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 2)

    def test_good(self):
        """When the guess is good the card should move to the hand"""
        self.plr.add_card(self.card, "hand")
        self.plr.deck.set("Province")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIn("Province", self.plr.hand)
        self.assertTrue(self.plr.deck.is_empty())

    def test_bad(self):
        """When the guess is bad the card should stay on the deck"""
        self.plr.add_card(self.card, "hand")
        self.plr.deck.set("Province")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertNotIn("Gold", self.plr.hand)
        self.assertNotIn("Province", self.plr.hand)
        self.assertEqual(self.plr.deck[-1].name, "Province")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
