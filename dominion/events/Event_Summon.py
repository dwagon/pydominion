#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Summon"""
import unittest

from dominion import Card, Game, Event, Player, PlayArea, Piles

SUMMON = "summon"


###############################################################################
class Event_Summon(Event.Event):
    """Summon Event"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PROMO
        self.desc = """Gain an Action card costing up to $4. Set it aside.
                If you did, then at the start of your next turn, play it."""
        self.name = "Summon"
        self.cost = 5

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Gain an Action card costing up to $4. Set it aside."""
        if SUMMON not in player.specials:
            player.specials[SUMMON] = PlayArea.PlayArea("Summon", game=game, initial=[])
        if card := player.plr_gain_card(4, types={Card.CardType.ACTION: True}, destination=player.specials[SUMMON]):
            if card.location == Piles.SPECIAL:
                player.secret_count += 1

    def hook_start_every_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        """If you did, then at the start of your next turn, play it."""
        if SUMMON in player.specials:
            for card in player.specials[SUMMON]:
                player.play_card(card, cost_action=False)
                player.secret_count -= 1
                del player.specials[SUMMON]

    def debug_dump(self, player: Player.Player) -> None:  # pragma: no coverage
        if SUMMON in player.specials:
            player.output(f"Summon Reserve: {self}: {player.specials[SUMMON]}")


###############################################################################
class TestSummon(unittest.TestCase):
    """Test Summon Event"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Summon"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Summon"]

    def test_with_treasure(self):
        """Use Summon"""
        self.plr.coins.add(6)
        self.plr.test_input = ["Get Moat"]
        self.plr.perform_event(self.event)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 7)  # Init 5 + 2 for moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
