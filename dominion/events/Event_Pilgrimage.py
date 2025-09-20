#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event, NoCardException, Player


###############################################################################
class Event_Pilgrimage(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Once per turn: Turn your Journey token over; then if it's face up,
        choose up to 3 differently named cards you have in play and gain a copy of each."""
        self.name = "Pilgrimage"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if not player.do_once("Pilgrimage"):
            player.output("Already performed a Pilgrimage this turn")
            return
        if not player.flip_journey_token():
            player.output("Flipped Journey token to face down")
            return
        selected = pick_cards(player)
        for card in selected:
            try:
                player.gain_card(card)
                player.output(f"Gained {card}")
            except NoCardException:
                player.output(f"No more {card}")


def pick_cards(player: Player.Player) -> list[str]:
    card_names = {_.name for _ in player.piles[Piles.PLAYED] if _.purchasable}
    selected: list[str] = []
    while True:
        choices = [("Finish", "")]
        for card_name in card_names:
            choices.append((card_name, card_name))

        if choice := player.plr_choose_options("Select a card to gain - up to 3!", *choices):
            selected.append(choice)
            card_names.remove(choice)
        else:
            break
        if len(selected) == 3:
            break
    return selected


###############################################################################
class Test_Pilgrimage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Pilgrimage"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Pilgrimage"]

    def test_play(self) -> None:
        """Perform a Pilgrimage"""
        self.plr.piles[Piles.PLAYED].set("Moat", "Silver", "Gold", "Copper", "Duchy")
        self.plr.test_input = ["moat", "silver", "finish"]
        self.plr.journey_token = False
        self.plr.coins.add(4)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Moat"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertTrue(self.plr.journey_token)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
