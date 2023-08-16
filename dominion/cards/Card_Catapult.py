#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Catapult(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.required_cards = ["Curse"]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+1 Coin; Trash a card from your hand.
            If it costs 3 or more, each other player gains a Curse.
            If it's a Treasure, each other player discards down to 3 cards in hand."""
        self.name = "Catapult"
        self.cost = 3
        self.coin = 1

    def special(self, game, player):
        cards = player.plr_trash_card(force=True)
        if not cards:
            return
        card = cards[0]
        for plr in player.attack_victims():
            if card.cost >= 3:
                plr.output(f"{player.name}'s Catapult Curses you")
                plr.gain_card("Curse")
            if card.isTreasure():
                plr.output(f"{player.name}'s Catapult forces you to discard down to 3 cards")
                plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Catapult(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Catapult"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Catapult"].remove()

    def test_play(self):
        """Play a Catapult with a non-treasure"""
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertIn("Duchy", self.g.trashpile)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])

    def test_play_treasure(self):
        """Play a Catapult with a treasure"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.victim.test_input = ["1", "2", "0"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Copper"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trashpile)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
