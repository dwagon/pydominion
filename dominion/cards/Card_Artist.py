#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Artist"""
import unittest
from collections import Counter

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Artist(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Action; +1 Card per card you have exactly one copy of in play."""
        self.name = "Artist"
        self.debtcost = 8
        self.actions = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+1 Card per card you have exactly one copy of in play."""
        card_counts = Counter[str]()
        for card in player.piles[Piles.PLAYED]:
            card_counts[card.name] += 1
        for count in card_counts.values():
            if count == 1:
                try:
                    player.pickup_card()
                except NoCardException:
                    player.output("No more cards")


###############################################################################
class TestArtist(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Artist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Artist")

    def test_play(self) -> None:
        """Play an Artist"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Silver", "Copper", "Copper", "Gold")
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2)  # -1 for playing; +3 for unique


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
