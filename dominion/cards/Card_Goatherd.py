#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Goatherd """

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Goatherd(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Action; You may trash a card from your hand.
            +1 Card per card the player to your right trashed on their last turn."""
        self.name = "Goatherd"
        self.cost = 3
        self.actions = 1

    def special(self, game, player):
        player.plr_trash_card()
        ptr = game.playerToRight(player)
        ctr = len(ptr.stats["trashed"])
        if ctr:
            player.output(f"Picking up {ctr} cards")
            player.pickup_cards(ctr)


###############################################################################
class Test_Goatherd(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Goatherd"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Goatherd")

    def test_play_this_turn(self):
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Province", "Estate")
        self.plr.piles[Piles.DECK].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.other.stats["trashed"] = ["Silver"]
        self.plr.test_input = ["Trash Province"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
