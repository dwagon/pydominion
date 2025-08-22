#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Magpie(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Card; +1 Action; Reveal the top card of your deck.
            If it's a Treasure, put it into your hand. If it's an Action or
            Victory card, gain a Magpie."""
        self.name = "Magpie"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal the top card of your deck. If it's a treasure, put it into your
        hand. If it's an Action or Victory card, gain a Magpie"""
        try:
            card = player.next_card()
        except NoCardException:
            return
        player.reveal_card(card)
        if card.isTreasure():
            player.output(f"Putting revealed {card} into hand")
            player.add_card(card, Piles.HAND)
        else:
            player.add_card(card, Piles.DECK)
            if card.isAction() or card.isVictory():
                try:
                    player.gain_card("Magpie")
                except NoCardException:
                    player.output("No more Magpies")
                else:
                    player.output(f"Revealed {card} so gaining Magpie")


###############################################################################
class Test_Magpie(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Magpie"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Magpie")

    def test_treasure(self) -> None:
        """Play a magpie with treasure"""
        self.plr.piles[Piles.DECK].set("Gold", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        # Hand of 5, the card gained and the treasure
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1 + 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_victory(self) -> None:
        """Play a magpie with treasure"""
        self.plr.piles[Piles.DECK].set("Duchy", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        # Hand of 5, the card gained
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertNotIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Magpie")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
