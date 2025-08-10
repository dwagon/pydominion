#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Poet"""
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Poet(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Sun; +1 Card; +1 Action; Reveal the top card of your deck. If it costs $3 or less, put it into your hand."""
        self.name = "Poet"
        self.cost = 4
        self.cards = 1
        self.actions = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal the top card of your deck. If it costs $3 or less, put it into your hand."""
        try:
            card = player.top_card()
        except NoCardException:
            return
        player.reveal_card(card)
        if card.cost <= 3 and not card.debtcost:
            player.output(f"{card} costs {card.cost} - putting into hand")
            player.pickup_card()
            return
        player.output(f"The next card is {card} - keeping it on deck")


###############################################################################
class Test_Poet(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Poet"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Poet")

    def test_play_cheap(self) -> None:
        """Play card - cheap on deck"""
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertNotIn("Copper", self.plr.piles[Piles.DECK])

    def test_play_expensive(self) -> None:
        """Play card - cheap on deck"""
        self.plr.piles[Piles.DECK].set("Silver", "Silver", "Silver", "Silver", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        new_card = self.plr.pickup_card()
        self.assertEqual(new_card.name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
