#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Bounty_Hunter """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bounty_Hunter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """+1 Action; Exile a card from your hand. If you didn't
            have a copy of it in Exile, +3 Coin."""
        self.name = "Bounty Hunter"
        self.cost = 4
        self.actions = 1

    def special(self, game, player):
        crd = player.card_sel(prompt="Exile a card", verbs=("Exile", "Unexile"))
        if crd:
            if not player.in_exile(crd[0].name):
                player.add_coins(3)
            player.hand.remove(crd[0])
            player.exile_card(crd[0])


###############################################################################
class Test_Bounty_Hunter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bounty Hunter"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Bounty Hunter"].remove()

    def test_play(self):
        self.plr.set_exile("Copper")
        self.plr.set_hand("Silver", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Exile Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
