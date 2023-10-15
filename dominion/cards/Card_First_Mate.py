#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/First_Mate"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_FirstMate(Card.Card):
    """First Mate"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Play any number of Action cards with the same name from your hand, 
        then draw until you have 6 cards in hand."""
        self.name = "First Mate"
        self.cost = 5

    def special(self, game, player):
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        options = [(f"Play {_.name}", _) for _ in actions]
        if actions:
            options.insert(0, ("Play nothing", None))
            to_play = player.plr_choose_options("Play which action?", *options)
            if to_play:
                for card in actions:
                    if card.name == to_play.name:
                        player.play_card(card, cost_action=False, discard=False)
        else:
            player.output("No suitable actions")
        while len(player.piles[Piles.HAND]) < 6:
            player.pickup_card()


###############################################################################
class TestFirstMate(unittest.TestCase):
    """Test First Mate"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["First Mate", "Market"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("First Mate")

    def test_play_card(self):
        """Play a card"""
        self.plr.piles[Piles.HAND].set("Market", "Market", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["1) Play Market"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 6)

    def test_play_no_actions(self):
        """Play a card with no suitable actions"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
