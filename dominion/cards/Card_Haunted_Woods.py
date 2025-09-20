#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_HauntedWoods(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Until you next turn, when any other player buys a card,
            he puts his hand on top of his deck in any order.
            At the start of your next turn: +3 Cards"""
        self.name = "Haunted Woods"
        self.cost = 5

    def duration(self, game, player):
        player.pickup_cards(3)

    def hook_all_players_buy_card(self, game, player, owner, card):
        if player == owner:
            return
        if player.has_defense(owner):
            return
        player.output(f"{owner}'s Haunted Woods puts your hand onto your deck")
        for crd in player.piles[Piles.HAND]:
            player.add_card(crd, Piles.TOPDECK)
            player.piles[Piles.HAND].remove(crd)
            player.output(f"Moving {crd} to deck")


###############################################################################
class TestHauntedWoods(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Haunted Woods"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Haunted Woods")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_buy(self):
        """Play a Haunted Woods"""
        self.vic.piles[Piles.HAND].set("Silver", "Duchy", "Province")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.vic.coins.set(6)
        self.vic.buy_card("Gold")
        self.assertIn("Silver", self.vic.piles[Piles.DECK])
        self.assertIn("Duchy", self.vic.piles[Piles.DECK])
        self.assertIn("Province", self.vic.piles[Piles.DECK])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
