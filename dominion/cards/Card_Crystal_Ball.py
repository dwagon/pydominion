#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Crystal_Ball"""

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_CrystalBall(Card.Card):
    """Crystal Ball"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """$1; Look at the top card of your deck. You may trash it, discard it, or, 
        if it's an Action or Treasure, play it."""
        self.coin = 1
        self.name = "Crystal Ball"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            next_card = player.next_card()
        except NoCardException:  # pragma: no coverage
            return
        options = [
            (f"Ignore {next_card}", "ignore"),
            (f"Trash {next_card}", "trash"),
            (f"Discard {next_card}", "discard"),
        ]
        if next_card.isTreasure() or next_card.isAction():
            options.append((f"Play {next_card}", "play"))
        action = player.plr_choose_options(f"What to do with {next_card}?", *options)
        match action:
            case "ignore":
                player.add_card(next_card, Piles.DECK)
            case "trash":
                player.trash_card(next_card)
            case "discard":
                player.discard_card(next_card)
            case "play":
                player.add_card(next_card, Piles.HAND)
                player.play_card(next_card, cost_action=False)


###############################################################################
class TestCrystalBall(unittest.TestCase):
    """Test Crystal Ball"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Crystal Ball", "Moat", "Horse"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Crystal Ball")

    def test_ignore(self) -> None:
        """Play a card and ignore"""
        self.plr.piles[Piles.DECK].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Ignore"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DECK])
        self.assertEqual(self.plr.coins.get(), coins + 1)

    def test_trash(self) -> None:
        """Play a card and trash"""
        self.plr.piles[Piles.DECK].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.g.trash_pile)

    def test_discard(self) -> None:
        """Play a card and discard"""
        self.plr.piles[Piles.DECK].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_play(self) -> None:
        """Play a card and play"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Moat")
        self.plr.piles[Piles.DISCARD].set(
            "Silver", "Silver", "Silver", "Silver", "Silver", "Silver"
        )
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 2 - 1
        )  # 2 from Moat, -1 played Crystal Ball

    def test_play_horse(self) -> None:
        """Play a card that moves itself (e.g. Horse)"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Horse")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play"]
        self.plr.play_card(self.card)
        self.assertNotIn("Horse", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Horse", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
