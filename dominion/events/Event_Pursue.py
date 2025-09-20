#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Pursue"""
import unittest

from dominion import Card, Game, Piles, Event, Player, NoCardException


###############################################################################
class Event_Pursue(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Buy; Name a card. Reveal the top 4 cards from your deck.
        Put the matches back and discard the rest."""
        self.name = "Pursue"
        self.cost = 2
        self.buys = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        options: list[tuple[str, str]] = [
            (f"Name {name}", name) for name, _ in sorted(game.get_card_piles())
        ]
        named_card = player.plr_choose_options("Name a card", *options)
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:
                break
            player.reveal_card(card)
            if card.name == named_card:
                player.add_card(card, Piles.DECK)
            else:
                player.discard_card(card)


###############################################################################
class TestPursue(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Pursue"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Pursue"]

    def test_pursue(self) -> None:
        """Use Pursue"""
        self.plr.coins.add(2)
        self.plr.piles[Piles.DECK].set("Moat", "Silver", "Gold", "Duchy")
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.card)
        self.g.print_state()
        self.assertIn("Moat", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
