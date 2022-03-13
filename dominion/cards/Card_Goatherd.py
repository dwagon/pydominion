#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Goatherd """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Goatherd(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """+1 Action; You may trash a card from your hand.
            +1 Card per card the player to your right trashed on their last turn."""
        self.name = "Goatherd"
        self.cost = 3
        self.actions = 1

    def special(self, game, player):
        player.plrTrashCard()
        ptr = game.playerToRight(player)
        ctr = len(ptr.stats["trashed"])
        if ctr:
            player.output("Picking up {} cards".format(ctr))
            player.pickup_cards(ctr)


###############################################################################
class Test_Goatherd(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Goatherd"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Goatherd"].remove()

    def test_play_this_turn(self):
        self.plr.set_hand("Copper", "Silver", "Gold", "Province", "Estate")
        self.plr.set_deck("Duchy")
        self.plr.add_card(self.card, "hand")
        self.other.stats["trashed"] = ["Silver"]
        self.plr.test_input = ["Trash Province"]
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertIsNone(self.plr.in_hand("Province"))
        self.assertIsNotNone(self.plr.in_hand("Duchy"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
