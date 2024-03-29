#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tiara """
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Tiara(Card.Card):
    """Tiara"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Buy; This turn, when you gain a card, you may put it onto your deck.
        You may play a Treasure from your hand twice."""
        self.name = "Tiara"
        self.cost = 4
        self.buys = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Play a treasure from your hand twice"""
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            return
        player.output("Select treasure that Tiara will let you play twice")
        player.move_card(self, Piles.PLAYED)
        if treasure := player.card_sel(cardsrc=treasures):
            for _ in range(2):
                player.play_card(treasure[0], discard=False, cost_action=False)
            if treasure[0].location == Piles.HAND:
                player.move_card(treasure[0], Piles.PLAYED)

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        """when you gain a card, you may put it onto your deck."""
        if player.plr_choose_options(
            f"Tiara lets you put {card} on top of your deck.",
            (f"Put {card} on top of your deck?", True),
            (f"Discard {card} as per normal?", False),
        ):
            return {OptionKeys.DESTINATION: "topdeck"}
        return {}


###############################################################################
class TestTiara(unittest.TestCase):
    """Test Tiara"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Tiara", "Investment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tiara")

    def test_play_deck(self) -> None:
        """Play a Tiara and put gained cards on to the deck"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.plr.test_input = ["Put"]
        self.plr.gain_card("Gold")
        self.assertIn("Gold", self.plr.piles[Piles.DECK])

    def test_discard(self) -> None:
        """Play a tiara and discard gained cards"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_treasure(self) -> None:
        """Play a tiara and play a treasure twice"""
        self.plr.piles[Piles.HAND].set("Copper", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Select Copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)  # Copper twice
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])

    def test_self_trasher(self) -> None:
        """Test playing a card that trashes itself"""
        self.plr.piles[Piles.HAND].set("Investment", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = [
            "Select Investment",
            "Trash Copper",
            "Trash this",
            "Trash Estate",
            "Trash this",
        ]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Investment", self.g.trash_pile)
        self.assertNotIn("Investment", self.plr.piles[Piles.PLAYED])
        self.assertIn("Estate", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
