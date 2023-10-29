#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Transport"""
import unittest
from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Transport(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Choose one: Exile an Action card from the Supply; 
        or put an Action card you have in Exile onto your deck."""
        self.name = "Transport"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        options = [
            ("Exile an Action card from Supply", True),
            ("Put an Action card you have in Exile onto you deck", False),
        ]
        if player.plr_choose_options("What to do with Transport?", *options):
            self.exile_action(game, player)
        else:
            self.exile_to_deck(player)

    def exile_action(self, game: "Game.Game", player: "Player.Player") -> None:
        """Exile an Action card from the Supply"""
        action_piles = game.get_action_piles()
        if piles := player.card_pile_sel(
            num=1, prompt="Exile an Action card from Supply", crdsrc=action_piles
        ):
            player.exile_card(piles[0])

    def exile_to_deck(self, player: "Player.Player") -> None:
        """put an Action card you have in Exile onto your deck"""

        if action := player.card_sel(
            prompt="Put an exiled action onto your deck",
            cardsrc=Piles.EXILE,
            types={Card.CardType.ACTION: True},
        ):
            player.move_card(action[0], Piles.DECK)


###############################################################################
class TestTransport(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Transport"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Transport"]

    def test_transport_exile(self) -> None:
        """Use Transport to exile Action"""
        self.plr.coins.add(3)
        self.plr.test_input = ["Exile an Action", "Moat"]
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.EXILE])

    def test_transport_exile_to_deck(self) -> None:
        """Use Transport to move an action from exile to deck"""
        self.plr.coins.add(3)
        self.plr.piles[Piles.EXILE].set("Moat", "Gold")
        self.plr.test_input = ["Put an action", "Moat"]
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DECK])
        self.assertNotIn("Moat", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
