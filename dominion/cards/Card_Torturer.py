#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Torturer(Card.Card):
    """Torturer"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+3 cards; Other players discard 2 cards or gain a curse"
        self.required_cards = ["Curse"]
        self.name = "Torturer"
        self.cards = 3
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player chooses one: he discards 2 cards; or
        he gains a Curse card, putting it in his hand"""
        for plr in player.attack_victims():
            plr.output("Choose:")
            self.choice_of_doom(plr, player)

    def choice_of_doom(self, victim: Player.Player, player: Player.Player) -> None:
        victim.output(f'Your hand is: {", ".join([c.name for c in victim.piles[Piles.HAND]])}')
        if victim.plr_choose_options(
            "Discard or curse",
            ("Discard 2 cards", True),
            ("Gain a curse card", False),
        ):
            player.output(f"{victim} discarded")
            victim.plr_discard_cards(2)
        else:
            player.output(f"{victim} opted for a curse")
            try:
                victim.gain_card("Curse", Piles.HAND)
            except NoCardException:
                player.output("No more Curses")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    if kind == "cards":
        return player.pick_to_discard(2)
    if kind == "choices":
        return True  # Discard
    return False


###############################################################################
class Test_Torturer(unittest.TestCase):
    """Test Torturer"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Torturer", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Torturer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_opt_curse(self) -> None:
        """Play the torturer - victim opts for a curse"""
        self.victim.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertIn("Curse", self.victim.piles[Piles.HAND])

    def test_opt_discard(self) -> None:
        """Play the torturer - victim opts for discarding"""
        self.victim.test_input = ["0", "1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)
        self.assertNotIn("Curse", self.victim.piles[Piles.HAND])

    def test_defended(self) -> None:
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
