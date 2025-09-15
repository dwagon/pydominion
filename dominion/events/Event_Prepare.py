#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Prepare"""
import unittest

from dominion import Card, Game, Piles, Event, PlayArea, Player

PREPARE = "prepare"


###############################################################################
class Event_Prepare(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Set aside your hand face up. At the start of your next turn, play those Actions and
                    Treasures in any order, then discard the rest."""
        self.name = "Prepare"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if PREPARE not in player.specials:
            player.specials[PREPARE] = PlayArea.PlayArea(initial=[])
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
            player.move_card(card, player.specials[PREPARE])
            player.secret_count += 1

    def hook_start_every_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if PREPARE not in player.specials:  # pragma: no coverage
            return
        player.output("Playing cards from Prepare")
        for card in player.specials[PREPARE]:
            if card.isAction() or card.isTreasure():
                player.play_card(card, cost_action=False)
            else:
                player.discard_card(card)
            player.secret_count -= 1
        del player.specials[PREPARE]


###############################################################################
class TestPrepare(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Prepare"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Prepare"]

    def test_play(self):
        """Use Prepare"""
        self.plr.coins.set(3)
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate", "Estate", "Estate", "Estate", "Estate")
        self.plr.piles[Piles.DISCARD].set("Copper", "Copper", "Copper", "Copper", "Copper")
        self.plr.piles[Piles.HAND].set("Gold", "Moat", "Province")
        self.plr.perform_event(self.card)
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)  # +2 for Moat
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
