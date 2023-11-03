#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Seer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+1 Card; +1 Action; Reveal the top 3 cards of your deck.
            Put the ones costing from 2 to 4 into your hand. Put the rest back in any order."""
        self.cards = 1
        self.actions = 1
        self.name = "Seer"
        self.cost = 5

    ###########################################################################
    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        drawn = []
        for _ in range(3):
            try:
                card = player.next_card()
            except NoCardException:
                break
            player.reveal_card(card)
            if card.cost in (2, 3, 4) and not card.potcost and not card.debtcost:
                player.output(f"Putting {card} into your hand")
                player.add_card(card, Piles.HAND)
            else:
                drawn.append(card)
        for card in drawn:
            player.output(f"Putting {card} back on deck")
            player.add_card(card, "topdeck")


###############################################################################
class Test_Seer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Seer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Seer")

    def test_play(self) -> None:
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Estate", "Province")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
