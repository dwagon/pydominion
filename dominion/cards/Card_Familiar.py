#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Familiar(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+1 card, +1 action; Each other player gains a Curse."
        self.name = "Familiar"
        self.cards = 1
        self.actions = 1
        self.cost = 3
        self.required_cards = ["Potion", "Curse"]
        self.potcost = True

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """All other players gain a curse"""
        for victim in player.attack_victims():
            try:
                victim.gain_card("Curse")
                player.output(f"{victim} got cursed")
                victim.output(f"{player}'s Familiar cursed you")
            except NoCardException:
                player.output("No more Curses")


###############################################################################
class Test_Familiar(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Familiar", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Familiar")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a familiar"""
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Curse")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_defended(self) -> None:
        self.victim.piles[Piles.HAND].set("Gold", "Moat")
        self.plr.play_card(self.card)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
