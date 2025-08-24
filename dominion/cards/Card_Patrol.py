#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, NoCardException, Player


###############################################################################
class Card_Patrol(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+3 Cards; Reveal the top 4 cards of your deck.
            Put the Victory cards and Curses into your hand.
            Put the rest back in any order."""
        self.name = "Patrol"
        self.cards = 3
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards = set()
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isVictory() or card.name == "Curse":
                player.add_card(card, Piles.HAND)
                player.output(f"Patrol adding {card}")
            else:
                cards.add(card)
        for card in cards:
            player.output(f"Putting {card} back on deck")
            player.add_card(card, Piles.TOPDECK)


###############################################################################
class Test_Patrol(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Patrol"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Patrol")

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Duchy", "Province", "Silver", "Gold", "Copper", "Copper", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
