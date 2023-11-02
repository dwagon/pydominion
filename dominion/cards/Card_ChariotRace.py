#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_ChariotRace(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+1 Action
        Reveal the top card of your deck and put it into your hand.
        The player to your left reveals the top card of their deck.
        If your card costs more, +1 Coin and +1 VP"""
        self.name = "Chariot Race"
        self.actions = 1
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            card = player.pickup_card()
        except NoCardException:
            return
        player.reveal_card(card)
        other = game.player_to_left(player)
        other_card = other.next_card()
        if not other_card:
            player.output(f"{other.name} doesn't have a suitable card")
            player.coins.add(1)
            player.add_score("Chariot Race")
            return
        if card.cost > other_card.cost:
            player.output(f"Your {card} costs more than {other.name}'s {other_card}")
            player.coins.add(1)
            player.add_score("Chariot Race")
        else:
            player.output(
                f"Your {card} costs less than {other.name}'s {other_card} - Getting nothing"
            )
        other.add_card(other_card, "topdeck")


###############################################################################
class TestChariotRace(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Chariot Race"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Chariot Race")

    def test_play_win(self) -> None:
        """Play a Chariot Race and win"""
        self.plr.piles[Piles.DECK].set("Gold")
        self.vic.piles[Piles.DECK].set("Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.score["Chariot Race"], 1)

    def test_play_lose(self) -> None:
        """Play a Chariot Race and lose"""
        self.plr.score["Chariot Race"] = 0
        self.plr.piles[Piles.DECK].set("Silver")
        self.vic.piles[Piles.DECK].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.score["Chariot Race"], 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
