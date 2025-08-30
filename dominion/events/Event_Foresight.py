#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Foresight"""
import unittest

from dominion import Card, Game, Piles, Event, Player, NoCardException

FORESIGHT = "foresight"


###############################################################################
class Event_Foresight(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Reveal cards from your deck until revealing an Action.
                    Set it aside and discard the rest. Put it into your hand at end of turn."""
        self.name = "Foresight"
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal cards from your deck until revealing an Action. Set it aside and discard the rest.
        Put it into your hand at end of turn."""
        player.specials[FORESIGHT] = []
        count = len(player.all_cards())
        while count:
            try:  # pragma: no coverage
                card = player.next_card()
            except NoCardException:
                break

            if card.isAction():
                player.output(f"Setting aside {card}")
                player.specials[FORESIGHT].append(card)
                player.secret_count += 1
                break
            player.discard_card(card)
            count -= 1
        else:
            player.output("No more actions in deck")
            return

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if not player.specials[FORESIGHT]:
            return
        card = player.specials[FORESIGHT][0]
        player.secret_count -= 1
        player.output(f"Adding {card} to hand from Foresight")
        player.add_card(card, Piles.HAND)


###############################################################################
class TestForesight(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Foresight"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Foresight"]

    def test_play(self) -> None:
        """Use Foresight"""
        self.plr.coins.set(2)
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Moat", "Estate", "Duchy")
        self.plr.perform_event(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 6)

    def test_play_no_actions(self) -> None:
        """Use Foresight with no actions"""
        self.plr.coins.set(2)
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Estate", "Duchy")
        self.plr.perform_event(self.card)
        self.plr.end_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
