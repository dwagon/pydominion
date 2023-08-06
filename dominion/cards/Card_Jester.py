#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Jester(Card.Card):
    """Jester"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+2 Coin. Each other player discards the top card of his deck.
            If it's a Victory card he gains a Curse. Otherwise either he gains a
            copy of the discarded card or you do, your choice."""
        self.name = "Jester"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        for plr in player.attack_victims():
            card = plr.next_card()
            if not card:
                player.output(f"{plr.name} has no cards!")
                continue
            plr.discard_card(card)
            plr.output(f"{player.name}'s Jester discarded your {card.name}")
            if card.isVictory():
                plr.output(f"{player.name}'s Jester cursed you")
                player.output(f"Cursed {plr.name}")
                plr.gain_card("Curse")
                continue
            getcard = player.plr_choose_options(
                f"Who should get a copy of {plr.name}'s {card.name}",
                (f"You get a {card.name}", True),
                ("{plr.name} gets a {card.name}", False),
            )
            if getcard:
                player.gain_card(card.name)
            else:
                plr.output(f"{player.name}'s Jester gave you a {card.name}")
                plr.gain_card(card.name)


###############################################################################
class Test_Jester(unittest.TestCase):
    """Test Jester"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Jester"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Jester"].remove()
        self.plr.add_card(self.card, "hand")

    def test_victory(self):
        """Play a jester with the victim having a Victory on top of deck"""
        self.victim.deck.set("Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Curse", self.victim.discardpile)
        self.assertIn("Duchy", self.victim.discardpile)

    def test_give_card(self):
        """Play a jester and give the duplicate to the victim"""
        self.victim.deck.set("Gold")
        self.plr.test_input = ["gets"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.discardpile.size(), 2)
        self.assertEqual(self.plr.discardpile.size(), 0)
        for c in self.victim.discardpile:
            self.assertEqual(c.name, "Gold")
        self.assertNotIn("Curse", self.victim.discardpile)
        self.assertIn("Gold", self.victim.discardpile)
        self.assertNotIn("Gold", self.plr.discardpile)

    def test_take_card(self):
        """Play a jester and take the duplicate from the victim"""
        self.victim.deck.set("Gold")
        self.plr.test_input = ["you"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.discardpile.size(), 1)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertNotIn("Curse", self.victim.discardpile)
        self.assertIn("Gold", self.victim.discardpile)
        self.assertIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
