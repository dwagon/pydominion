#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sea_Chart"""

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Sea_Chart(Card.Card):
    """Sea Chart"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Card; +1 Action; Reveal the top card of your deck.
            If you have a copy of it in play, put it into your hand."""
        self.name = "Sea Chart"
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Sea Chart Special"""
        try:
            next_card = player.piles[Piles.DECK].top_card()
        except NoCardException:
            player.output("No cards on deck")
            return
        player.reveal_card(next_card)
        if next_card.name in player.piles[Piles.PLAYED]:
            player.output(f"Next card is {next_card}, same as played so moving to hand")
            player.move_card(next_card, Piles.HAND)
        else:
            player.output(f"Next card is {next_card} which hasn't been played")


###############################################################################
class Test_Sea_Chart(unittest.TestCase):
    """Test Sea_Chart"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sea Chart", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sea Chart")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card_match(self) -> None:
        """Play a Sea Chart where we have played the same"""
        self.plr.piles[Piles.DECK].set("Moat", "Copper")
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_card_no_match(self) -> None:
        """Play a Sea Chart where we haven't played the same"""
        self.plr.piles[Piles.DECK].set("Moat", "Copper")
        self.plr.piles[Piles.PLAYED].set("Copper")
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
