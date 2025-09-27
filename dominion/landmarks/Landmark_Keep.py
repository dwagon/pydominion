#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Keep"""
import unittest

from dominion import Card, Game, Piles, Landmark, Player


###############################################################################
class Landmark_Keep(Landmark.Landmark):
    """Keep"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, 5VP per differently named Treasure you have,
        that you have more copies of than each other player, or tied for most."""
        self.name = "Keep"

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        """Scoring"""
        cards = card_counts(game)

        # If player is the one who has the most, gain the points
        for card_name, details in cards.items():
            m = max(details.values())
            if player.name in details and details[player.name] == m:
                player.output(f"Gaining 5 from Landmark as you have the most {card_name} ({m})")
                player.add_score("Keep", 5)


###############################################################################
def card_counts(game: "Game.Game") -> dict[str, dict[str, int]]:
    """For each type of treasure card work out who has how many"""
    cards: dict[str, dict[str, int]] = {}  # CardName: PlayerName: Count
    for plr in game.player_list():
        for card in plr.all_cards():
            if card.isTreasure():
                if card.name not in cards:
                    cards[card.name] = {}
                cards[card.name][plr.name] = cards[card.name].get(plr.name, 0) + 1
    return cards


###############################################################################
class Test_Keep(unittest.TestCase):
    """Test Keep"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            landmarks=["Keep"],
            badcards=[
                "Shepherd",
                "Tracker",
                "Fool",
                "Cemetery",
                "Pooka",
                "Pixie",
                "Secret Cave",
            ],
        )
        self.g.start_game()
        self.plr, self.other = self.g.player_list()

    def test_most(self) -> None:
        """Use Keep when we have the most Silver"""
        self.plr.piles[Piles.DECK].set("Silver")
        self.plr.game_over()
        try:
            self.assertEqual(self.plr.get_score_details()["Keep"], 5)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_card_counts(self) -> None:
        """Test card_counts()"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Estate", "Duchy")
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.other.piles[Piles.DECK].set("Silver", "Gold", "Estate", "Duchy")
        self.other.piles[Piles.HAND].set("Gold", "Silver")
        cards = card_counts(self.g)
        self.assertNotIn("Duchy", cards)
        self.assertEqual(cards["Copper"], {self.plr.name: 1})
        self.assertEqual(cards["Silver"], {self.plr.name: 2, self.other.name: 2})
        self.assertEqual(cards["Gold"], {self.plr.name: 1, self.other.name: 2})


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
