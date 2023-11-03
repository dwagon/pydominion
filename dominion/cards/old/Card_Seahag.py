#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, NoCardException


###############################################################################
class Card_Seahag(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Each other player discards the top card of his deck, then gains a Curse card,
            putting it on top of his deck"""
        self.required_cards = ["Curse"]
        self.name = "Sea Hag"
        self.cost = 4

    def special(self, game, player):
        """Each other player discards the top card of his deck,
        then gains a Curse card, putting it on top of his deck"""
        for pl in player.attack_victims():
            try:
                card = pl.next_card()
            except NoCardException:
                break
            pl.discard_card(card)
            pl.output(f"Discarded your {card}")
            pl.gain_card("Curse", destination="topdeck")
            pl.output(f"Got cursed by {player.name}'s Sea Hag")
            player.output("{pl.name} got cursed")


###############################################################################
class Test_Seahag(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, oldcards=True, initcards=["Sea Hag", "Moat"]
        )
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.seahag = self.g.get_card_from_pile("Sea Hag")
        self.mcard = self.g.get_card_from_pile("Moat")
        self.attacker.add_card(self.seahag, Piles.HAND)

    def test_defended(self):
        self.victim.add_card(self.mcard, Piles.HAND)
        self.attacker.play_card(self.seahag)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 6)
        self.assertNotEqual(self.victim.piles[Piles.DECK][0].name, "Curse")
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_nodefense(self):
        self.victim.piles[Piles.DECK].set("Gold")
        self.attacker.play_card(self.seahag)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Gold")
        self.assertEqual(self.victim.piles[Piles.DECK][0].name, "Curse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
