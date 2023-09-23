#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Soothsayer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.GUILDS
        self.desc = "Gain a Gold. Each other player gains a Curse. Each player who did draws a card."
        self.required_cards = ["Curse"]
        self.name = "Soothsayer"
        self.cost = 5

    def special(self, game, player):
        player.gain_card("Gold")
        for pl in player.attack_victims():
            player.output(f"{pl.name} got cursed")
            pl.output("f{player.name}'s Soothsayer cursed you")
            pl.gain_card("Curse")
            pl.pickup_card()


###############################################################################
class Test_Soothsayer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Soothsayer"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.wcard = self.g.get_card_from_pile("Soothsayer")
        self.attacker.add_card(self.wcard, Piles.HAND)

    def test_play(self):
        self.attacker.play_card(self.wcard)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 6)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.attacker.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
