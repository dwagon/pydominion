#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Necromancer"""

import unittest

from dominion import Card, PlayArea, Game, Piles, Player

NECROMANCER = "necromancer"


###############################################################################
class Card_Necromancer(Card.Card):
    """Necromancer"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Choose a face up, non-Duration Action card in the trash.
            Turn it face down for the turn, and play it, leaving it there."""
        self.name = "Necromancer"
        self.cost = 4
        self.required_cards = [
            ("Card", "Zombie Apprentice"),
            ("Card", "Zombie Mason"),
            ("Card", "Zombie Spy"),
        ]

    def setup(self, game: "Game.Game") -> None:
        game.specials[NECROMANCER] = PlayArea.PlayArea(name="Necromancer")

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        game.specials[NECROMANCER] = PlayArea.PlayArea(name="Necromancer")

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Play a non-Duration Action card from the trash, leaving it there."""
        action_cards = [
            _ for _ in game.trash_pile if _.isAction() and not _.isDuration() and _ not in game.specials[NECROMANCER]
        ]
        if cards := player.card_sel(cardsrc=action_cards, prompt="Select Action card from Trash"):
            game.specials[NECROMANCER].add(cards[0])
            player.play_card(cards[0], discard=False, cost_action=False, move_card=False)


###############################################################################
class TestNecromancer(unittest.TestCase):
    """Test Necromancer"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Necromancer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.plr.get_card_from_pile("Necromancer")
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
