#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_ChariotRace(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = """+1 Action
        Reveal the top card of your deck and put it into your hand.
        The player to your left reveals the top card of their deck.
        If your card costs more, +1 Coin and +1 VP"""
        self.name = "Chariot Race"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        card = player.pickup_card()
        player.reveal_card(card)
        other = game.player_to_left(player)
        othercard = other.next_card()
        if card.cost > othercard.cost:
            player.output(
                f"Your {card.name} costs more than {other.name}'s {othercard.name}"
            )
            player.add_coins()
            player.add_score("Chariot Race")
        else:
            player.output(
                f"Your {card.name} costs less than {other.name}'s {othercard.name} - Getting nothing"
            )
        other.add_card(othercard, "topdeck")


###############################################################################
class Test_ChariotRace(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Chariot Race"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Chariot Race"].remove()

    def test_play_win(self):
        """Play a Chariot Race and win"""
        self.plr.deck.set("Gold")
        self.vic.deck.set("Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertIn("Gold", self.plr.hand)
        self.assertEqual(self.plr.score["Chariot Race"], 1)

    def test_play_lose(self):
        """Play a Chariot Race and lose"""
        self.plr.score["Chariot Race"] = 0
        self.plr.deck.set("Silver")
        self.vic.deck.set("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertIn("Silver", self.plr.hand)
        self.assertEqual(self.plr.score["Chariot Race"], 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
