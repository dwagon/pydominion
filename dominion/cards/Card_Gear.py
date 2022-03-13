#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game


###############################################################################
class Card_Gear(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = (
            "+2 Cards; Set aside up to 2 cards from your hand. Pick up next turn"
        )
        self.name = "Gear"
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """Set aside up to 2 cards from your hand face down..."""
        if not hasattr(player, "gear_reserve"):
            player.gear_reserve = PlayArea.PlayArea([])
        cards = player.cardSel(
            num=2,
            cardsrc="hand",
            prompt="Set aside up to 2 cards from your hand to be put back next turn",
            verbs=("Set", "Unset"),
        )
        for card in cards:
            player.gear_reserve.add(card)
            player.hand.remove(card)
            player.secret_count += 1

    def duration(self, game, player):
        """... At the start of your next turn, put them into your hand"""
        for card in player.gear_reserve[:]:
            player.output("Pulling %s reserved by Gear" % card.name)
            player.add_card(card, "hand")
            player.gear_reserve.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_Gear(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Gear"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Gear"].remove()

    def test_playcard(self):
        """Play a gear"""
        self.plr.set_hand("Duchy", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["set silver", "set gold", "finish"]
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.hand.size(), 1 + 2)  # Duchy + 2 picked up
            self.assertIsNotNone(self.plr.in_hand("Duchy"))
            self.assertEqual(self.plr.durationpile.size(), 1)
            self.plr.end_turn()
            self.plr.start_turn()
            self.assertEqual(self.plr.durationpile.size(), 0)
            self.assertEqual(self.plr.played.size(), 1)
            self.assertEqual(self.plr.played[-1].name, "Gear")
            self.assertIsNotNone(self.plr.in_hand("Silver"))
            self.assertIsNotNone(self.plr.in_hand("Gold"))
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
