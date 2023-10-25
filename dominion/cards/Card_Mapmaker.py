#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Mapmaker"""

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Mapmaker(Card.Card):
    """Mapmaker"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Look at the top 4 cards of your deck. Put 2 into your hand and discard the rest.
        When any player gains a Victory card, you may play this from your hand."""
        self.name = "Mapmaker"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if top_4 := [player.next_card() for _ in range(4)]:
            to_hand = player.card_sel(
                prompt="Pick 2 to put into your hand", num=2, cardsrc=top_4
            )
            if not to_hand:
                return

            for card in top_4:
                assert card is not None
                if card in to_hand:
                    player.add_card(card, Piles.HAND)
                else:
                    player.add_card(card, Piles.DECK)


###############################################################################
class TestMapmaker(unittest.TestCase):
    """Test Mapmaker"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Mapmaker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mapmaker")

    def test_play(self) -> None:
        """Play Card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Estate", "Silver", "Gold", "Duchy", "Province")
        self.plr.test_input = ["Select Silver -", "Select Gold", "Finish"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
