#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Alchemist"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Alchemist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+2 cards, +1 action; At the start of Clean-up this turn, if you have a Potion in play, you may put this onto your deck."
        self.name = "Alchemist"
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = True
        self.required_cards = ["Potion"]

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> None:
        """At the start of Clean-up this turn, if you have a Potion in play, you may put this onto your deck."""
        if not "Potion" in player.piles[Piles.PLAYED]:
            return
        if player.plr_choose_options(
            "What to do with the alchemist?",
            ("Discard alchemist", False),
            ("Put on top of deck", True),
        ):
            player.move_card(self, "topdeck")


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Alchemist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.alchemist = self.g.get_card_from_pile("Alchemist")
        self.plr.add_card(self.alchemist, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.alchemist)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_nopotion(self):
        """Discard Alchemist with no potion in play"""
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 8)  # 5 for hand, +2 cards, alch

    def test_discard(self):
        """Discard an Alchemist even if we have a potion in play"""
        self.plr.piles[Piles.PLAYED].set("Potion")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 9)  # 5 for hand, +2 cards, alch, pot
        self.assertIn("Alchemist", self.plr.piles[Piles.DISCARD])

    def test_keep(self):
        """Keep an Alchemist for next turn"""
        self.plr.piles[Piles.PLAYED].set("Potion")
        self.plr.test_input = ["top of deck"]
        self.plr.play_card(self.alchemist)
        self.plr.cleanup_phase()
        self.assertIn("Alchemist", self.plr.piles[Piles.HAND])
        self.assertNotIn("Alchemist", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
