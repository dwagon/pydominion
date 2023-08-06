#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Survivors """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Survivors(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.purchasable = False
        self.cost = 0
        self.desc = "Look at the top 2 cards of your deck. Discard them or put them back in any order."
        self.name = "Survivors"

    def special(self, game, player):
        """Look at the top 2 cards of your deck. Discard them or
        put them back in any order"""
        crds = player.pickup_cards(2)
        ans = player.plr_choose_options(
            "What to do with survivors?",
            (f"Discard {crds[0].name} and {crds[1].name}", "discard"),
            (f"Return {crds[0].name} and {crds[1].name} to deck", "return"),
        )
        if ans == "discard":
            player.discard_card(crds[0])
            player.discard_card(crds[1])
        else:
            player.add_card(crds[0], "deck")
            player.add_card(crds[1], "deck")


###############################################################################
class Test_Survivors(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Ruins"].remove()
            if self.card.name == "Survivors":
                break
        self.plr.add_card(self.card, "hand")

    def test_play_discard(self):
        """Play a survivor and discard cards"""
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertNotIn("Gold", self.plr.hand)
        self.assertNotIn("Silver", self.plr.hand)

    def test_play_keep(self):
        """Play a survivor and keep cards"""
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Return"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.discardpile)
        self.assertNotIn("Silver", self.plr.discardpile)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Silver", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
