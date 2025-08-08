#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Rice_Broker"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Rice_Broker(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = (
            """+1 Action; Trash a card from your hand. If it's a Treasure, +2 Cards. If it's an Action, +5 Cards."""
        )
        self.name = "Rice Broker"
        self.cost = 5
        self.actions = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. If it's a Treasure, +2 Cards. If it's an Action, +5 Cards."""
        if cards := player.plr_trash_card(num=1):
            card = cards[0]
            if card.isTreasure():
                player.pickup_cards(num=2)
            if card.isAction():
                player.pickup_cards(num=5)


###############################################################################
class Test_Rice_Broker(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Rice Broker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Rice Broker")

    def test_play_treasure(self) -> None:
        """Play card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Trash Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.g.trash_pile)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 2)  # -1 for playing, -1 for trashing

    def test_play_action(self) -> None:
        """Play card and trash action"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Rice Broker")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Rice Broker"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 5 - 1 - 1)  # -1 for played, -1 for trashed


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
