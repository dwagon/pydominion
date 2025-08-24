#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Bandit"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, NoCardException, Player


###############################################################################
class Card_Bandit(Card.Card):
    """Bandit"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = """Gain a Gold. Each other player reveals the top 2 cards
            of their deck, trashes a revealed Treasure other than Copper, and
            discards the rest."""
        self.name = "Bandit"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.gain_card("Gold")
        for plr in player.attack_victims():
            thieve_on(victim=plr, bandit=player)


def thieve_on(victim: Player.Player, bandit: Player.Player) -> None:
    """Each other player reveals the top 2 cards of their deck,
    trashes a revealed Treasure other than Copper, and discards the rest."""
    # Each other player reveals the top 2 cards of their deck
    treasures = []
    for _ in range(2):
        try:
            card = victim.next_card()
        except NoCardException:
            continue
        victim.reveal_card(card)
        if card.isTreasure() and card.name != "Copper":
            treasures.append(card)
        else:
            card.location = Piles.CARDPILE
            victim.add_card(card, Piles.DISCARD)
    if not treasures:
        bandit.output(f"Player {victim} has no suitable treasures")
        return

    choices: list[tuple[str, Any]] = [("Don't trash any card", None)]
    for _ in treasures:
        choices.append((f"Trash {_} from {victim}", _))

    card = bandit.plr_choose_options(f"What to do to {victim}'s cards?", *choices)
    # Discard the ones we don't care about
    for treasure in treasures:
        if card == treasure:
            card.location = None
            victim.trash_card(card)
            bandit.output(f"Trashed {card} from {victim}")
            victim.output(f"{bandit}'s Bandit trashed your {card}")
        else:
            victim.add_card(treasure, Piles.DISCARD)


###############################################################################
class TestBandit(unittest.TestCase):
    """Test Bandit"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Bandit"])
        self.g.start_game()
        self.thief, self.vic = self.g.player_list()
        self.thief.name = "MrBandit"
        self.vic.name = "MrVic"
        self.card = self.g.get_card_from_pile("Bandit")
        self.thief.add_card(self.card, Piles.HAND)

    def test_do_nothing(self) -> None:
        """Don't trash anything"""
        self.vic.piles[Piles.HAND].set("Copper", "Copper")
        self.vic.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.test_input = ["Don't trash"]
        self.thief.play_card(self.card)
        self.assertEqual(self.vic.piles[Piles.DECK].size(), 1)
        self.assertEqual(self.vic.piles[Piles.DISCARD].size(), 2)

    def test_trash_treasure(self) -> None:
        """Trash the treasure"""
        self.vic.piles[Piles.HAND].set("Copper", "Copper")
        self.vic.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.test_input = ["trash gold"]
        self.thief.play_card(self.card)
        # Make sure the gold ends up in the trash pile and not in the victims deck
        self.assertIn("Gold", self.g.trash_pile)
        for card in self.vic.piles[Piles.DECK]:
            self.assertNotEqual(card.name, "Gold")
        self.assertEqual(self.vic.piles[Piles.DISCARD][0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
