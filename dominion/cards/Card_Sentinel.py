#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sentinel"""

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Sentinel(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Sentinel"
        self.desc = """Look at the top 5 cards of your deck. You may trash up to 2 of them.
        Put the rest back in any order."""
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards: list[Card.Card] = []
        for _ in range(5):
            try:
                cards.append(player.next_card())
            except NoCardException:
                break
        if not cards:
            player.output("No suitable cards")
            return
        player.output("Trash up to 2 of these")
        trashed = player.plr_trash_card(num=2, cardsrc=cards)
        for card in cards:
            if card not in trashed:
                player.add_card(card, "topdeck")


###############################################################################
class TestSentinel(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sentinel"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sentinel")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the card"""
        self.plr.piles[Piles.DECK].set(
            "Province", "Copper", "Silver", "Gold", "Estate", "Duchy"
        )
        self.plr.test_input = ["Trash Copper", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
