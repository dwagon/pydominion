#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Necromancer"""

import unittest
from typing import Any

from dominion import Card, PlayArea, Game, Piles, Player, OptionKeys

NECROMANCER = "necromancer"


###############################################################################
class Card_Necromancer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Play a non-Duration Action card from the trash, leaving it there."
        self.name = "Necromancer"
        self.cost = 4
        self.required_cards = [
            ("Card", "Zombie Apprentice"),
            ("Card", "Zombie Mason"),
            ("Card", "Zombie Spy"),
        ]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Play a non-Duration Action card from the trash, leaving it there."""
        action_cards = [
            _ for _ in game.trash_pile if _.isAction() and not _.isDuration() and _ not in game.specials[NECROMANCER]
        ]
        if card := player.card_sel(cardsrc=action_cards, prompt="Select Action card from Trash"):
            game.specials[NECROMANCER].add(card[0])
            player.play_card(card[0], discard=False, cost_action=False)

    def setup(self, game: Game.Game) -> None:
        """Use a play area to keep track of what has been played by Necromancer this turn"""
        game.specials[NECROMANCER] = PlayArea.PlayArea()

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """Reset what has been played by Necromancer"""
        game.specials[NECROMANCER].empty()
        return {}


###############################################################################
class TestNecromancer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Necromancer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Necromancer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Necromancer"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver")
        self.plr.test_input = ["Select Zombie Spy", "Keep Gold"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])  # From Zombie Spy
        self.assertIn("Zombie Spy", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
