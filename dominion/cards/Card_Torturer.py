#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Torturer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+3 cards; Other players discard 2 cards or gain a curse"
        self.required_cards = ["Curse"]
        self.name = "Torturer"
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """Each other player chooses one: he discards 2 cards; or
        he gains a Curse card, putting it in his hand"""
        for plr in player.attack_victims():
            plr.output("Choose:")
            self.choiceOfDoom(plr, player)

    def choiceOfDoom(self, victim, player):
        victim.output("Your hand is: %s" % ", ".join([c.name for c in victim.piles[Piles.HAND]]))
        discard = victim.plr_choose_options(
            "Discard or curse", ("Discard 2 cards", True), ("Gain a curse card", False)
        )
        if discard:
            player.output("%s discarded" % victim.name)
            victim.plr_discard_cards(2)
        else:
            player.output("%s opted for a curse" % victim.name)
            victim.gain_card("Curse", Piles.HAND)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if kind == "cards":
        return player.pick_to_discard(2)
    if kind == "choices":
        return True  # Discard
    return False


###############################################################################
class Test_Torturer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Torturer", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Torturer"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_opt_curse(self):
        """Play the torturer - victim opts for a curse"""
        self.victim.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertIn("Curse", self.victim.piles[Piles.HAND])

    def test_opt_discard(self):
        """Play the torturer - victim opts for discarding"""
        self.victim.test_input = ["0", "1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)
        self.assertNotIn("Curse", self.victim.piles[Piles.HAND])

    def test_defended(self):
        """Defending against a torturer"""
        self.victim.piles[Piles.HAND].set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 1)
        self.assertNotIn("Curse", self.victim.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
