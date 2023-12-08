#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Tools"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Tools(Card.Card):
    """Tools"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Gain a copy of a card anyone has in play."""
        self.name = "Tools"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain a copy of a card anyone has in play."""
        available: set[str] = set(["Tools"])
        for plr in game.player_list():
            for card in plr.piles[Piles.PLAYED]:
                available.add(card.name)
            for card in plr.piles[Piles.DURATION]:
                available.add(card.name)
        options: list[tuple[str, str | None]] = [("Gain nothing", None)]
        options.extend((f"Gain {card_name}", card_name) for card_name in available)
        if to_gain := player.plr_choose_options("Gain which card?", *options):
            try:
                player.gain_card(to_gain)
            except NoCardException:
                player.output(f"No more {to_gain}")


###############################################################################
class TestTools(unittest.TestCase):
    """Test Tools"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Tools"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tools")

    def test_play(self) -> None:
        """Play Card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Silver", "Gold")
        self.plr.test_input = ["Gain Gold"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
