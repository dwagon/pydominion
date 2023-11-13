#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Jester(Card.Card):
    """Jester"""

    def __init__(self) -> None:
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

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            try:
                card = plr.next_card()
            except NoCardException:
                player.output(f"{plr} has no cards!")
                continue
            plr.discard_card(card)
            plr.output(f"{player}'s Jester discarded your {card}")
            if card.isVictory():
                plr.output(f"{player.name}'s Jester cursed you")
                player.output(f"Cursed {plr}")
                plr.gain_card("Curse")
                continue
            if player.plr_choose_options(
                f"Who should get a copy of {plr}'s {card}",
                (f"You get a {card}", True),
                (f"{plr} gets a {card}", False),
            ):
                player.gain_card(card.name)
            else:
                plr.output(f"{player.name}'s Jester gave you a {card}")
                plr.gain_card(card.name)


###############################################################################
class Test_Jester(unittest.TestCase):
    """Test Jester"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Jester"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Jester")
        self.plr.add_card(self.card, Piles.HAND)

    def test_victory(self) -> None:
        """Play a jester with the victim having a Victory on top of deck"""
        self.victim.piles[Piles.DECK].set("Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.victim.piles[Piles.DISCARD])

    def test_give_card(self) -> None:
        """Play a jester and give the duplicate to the victim"""
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.test_input = ["gets"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        for c in self.victim.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Gold")
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_take_card(self) -> None:
        """Play a jester and take the duplicate from the victim"""
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.test_input = ["you"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
