#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Survivors """

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Survivors(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.purchasable = False
        self.cost = 0
        self.desc = "Look at the top 2 cards of your deck. Discard them or put them back in any order."
        self.name = "Survivors"
        self.pile = "Ruins"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Look at the top 2 cards of your deck. Discard them or
        put them back in any order"""
        cards = player.pickup_cards(2)
        if len(cards) < 2:  # pragma: no coverage
            player.output("Insufficient cards")
            return
        if player.plr_choose_options(
            "What to do with survivors?",
            (f"Discard {cards[0]} and {cards[1]}", True),
            (f"Return {cards[0]} and {cards[1]} to deck", False),
        ):
            player.discard_card(cards[0])
            player.discard_card(cards[1])
        else:
            player.move_card(cards[0], Piles.DECK)
            player.move_card(cards[1], Piles.DECK)


###############################################################################
class TestSurvivors(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Ruins")
            if self.card.name == "Survivors":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_discard(self) -> None:
        """Play a survivor and discard cards"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.DECK])
        self.assertNotIn("Silver", self.plr.piles[Piles.DECK])

    def test_play_return(self) -> None:
        """Play a survivor and return to deck"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].empty()
        self.plr.test_input = ["Return"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
