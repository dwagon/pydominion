#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Pilgrimage(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Once per turn: Turn your Journey token over; then if it's face up,
        choose up to 3 differently named cards you have in play and gain a copy of each."""
        self.name = "Pilgrimage"
        self.cost = 4

    def special(self, game, player):
        if not player.do_once("Pilgrimage"):
            player.output("Already performed a Pilgrimage this turn")
            return
        if not player.flip_journey_token():
            player.output("Flipped Journey token to face down")
            return
        cardnames = {c.name for c in player.piles[Piles.PLAYED] if c.purchasable}
        selected = []
        while True:
            choices = [
                ("Finish", None),
            ]
            for card_name in cardnames:
                choices.append((card_name, card_name))

            if choice := player.plr_choose_options("Select a card to gain - up to 3!", *choices):
                selected.append(choice)
                cardnames.remove(choice)
            else:
                break
            if len(selected) == 3:
                break
        for card in selected:
            player.gain_card(card)
            player.output(f"Gained {card}")


###############################################################################
class Test_Pilgrimage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Pilgrimage"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Pilgrimage"]

    def test_play(self):
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
