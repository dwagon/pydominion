#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Mountain_Shrine"""
import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Mountain_Shrine(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Sun; +$2; You may trash a card from your hand. Then if there are any Action cards in the trash, +2 Cards."""
        self.name = "Mountain Shrine"
        self.coin = 2
        self.debtcost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash a card from your hand. Then, if there are any Action cards in the trash, +2 Cards."""
        if player.plr_trash_card(num=1):
            for card in game.trash_pile:
                if card.isAction():
                    player.pickup_cards(num=2)
                    break


###############################################################################
class Test_Mountain_Shrine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mountain Shrine")

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.g.trash_pile)

    def test_play_with_trash(self) -> None:
        """Play card when action in trash"""
        self.g.trash_pile.set("Mountain Shrine")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DECK].set("Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Copper"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 1 - 1)  # -1 for played, -1 for trashed


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
