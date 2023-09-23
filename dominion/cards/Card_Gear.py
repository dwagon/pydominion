#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game, Piles


###############################################################################
class Card_Gear(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+2 Cards; Set aside up to 2 cards from your hand. Pick up next turn"
        self.name = "Gear"
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """Set aside up to 2 cards from your hand face down..."""
        if not hasattr(player, "gear_reserve"):
            player.gear_reserve = PlayArea.PlayArea([])
        cards = player.card_sel(
            num=2,
            cardsrc=Piles.HAND,
            prompt="Set aside up to 2 cards from your hand to be put back next turn",
            verbs=("Set", "Unset"),
        )
        for card in cards:
            player.gear_reserve.add(card)
            player.piles[Piles.HAND].remove(card)
            player.secret_count += 1

    def duration(self, game, player):
        """... At the start of your next turn, put them into your hand"""
        for card in player.gear_reserve:
            player.output("Pulling %s reserved by Gear" % card.name)
            player.add_card(card, Piles.HAND)
            player.gear_reserve.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_Gear(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Gear"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Gear")

    def test_playcard(self):
        """Play a gear"""
        self.plr.piles[Piles.HAND].set("Duchy", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["set silver", "set gold", "finish"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 2)  # Duchy + 2 picked up
            self.assertIn("Duchy", self.plr.piles[Piles.HAND])
            self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
            self.plr.end_turn()
            self.plr.start_turn()
            self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
            self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
            self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Gear")
            self.assertIn("Silver", self.plr.piles[Piles.HAND])
            self.assertIn("Gold", self.plr.piles[Piles.HAND])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
